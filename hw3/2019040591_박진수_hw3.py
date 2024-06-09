import sys
import math


def load_data(filename, label_dict) -> list:
    dataset = []
    with open(filename, 'r') as file:
        for line in file:
            elements = line.strip().split('\t')
            object_id = int(elements[0])
            x_coord = float(elements[1])
            y_coord = float(elements[2])
            dataset.append((object_id, x_coord, y_coord))
            label_dict[object_id] = 0  # undefined
        return dataset


def get_distance(point1, point2) -> float:
    return math.sqrt((point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2)


def dbscan(dataset, dist_func, eps, min_pts, label_dict) -> None:
    cluster_id = 0
    for point in dataset:
        if label_dict[point[0]] != 0:  # point -> (0, 84.768997, 33.368999)
            continue
        neighbors = range_query(dataset, dist_func, point, eps)
        if len(neighbors) < min_pts:
            label_dict[point[0]] = -1  # Noise
            continue
        cluster_id += 1
        label_dict[point[0]] = cluster_id
        seed_set = set(neighbors)
        seed_set.discard(point)

        while seed_set:
            current_point = seed_set.pop()
            current_id = current_point[0]

            if label_dict[current_id] == -1:  # Change label from noise to border point
                label_dict[current_id] = cluster_id
            if label_dict[current_id] != 0:  # Skip if already processed
                continue

            # Label the point with the cluster ID
            label_dict[current_id] = cluster_id

            # Expand cluster with neighbors if condition meets
            current_neighbors = range_query(dataset, dist_func, current_point, eps)
            if len(current_neighbors) >= min_pts:
                new_points = {tuple(n) for n in current_neighbors if label_dict[n[0]] <= 0}
                seed_set.update(new_points)


def range_query(labeled_dataset, dist_func, q, eps) -> list:
    neighbors = set()
    for point in labeled_dataset:
        if dist_func(q, point) <= eps:
            neighbors.add(tuple(point))
    return list(neighbors)


def group_by_cluster(label_dict) -> dict:
    cluster_groups = {}
    for object_id, cluster_id in label_dict.items():
        if cluster_id in cluster_groups:
            cluster_groups[cluster_id].append(object_id)
        else:
            cluster_groups[cluster_id] = [object_id]
    del cluster_groups[-1]
    return cluster_groups


def sort_n_groups_by_size(cluster_groups, n) -> list:
    sorted_groups = sorted(cluster_groups.items(), key=lambda item: len(item[1]), reverse=True)[:n]
    return sorted_groups


def write_clusters(sorted_n_groups, output_prefix) -> None:
    for idx, objects in enumerate(sorted_n_groups):
        with open(f'{output_prefix}_cluster_{idx}.txt', 'w') as f:
            for obj_id in objects[1]:
                f.write(f'{obj_id}\n')


def main(input_data_file_name, n, eps, min_pts):
    n = int(n)
    eps = float(eps)
    min_pts = int(min_pts)

    label_dict = {}

    dataset = load_data(input_data_file_name, label_dict)
    dbscan(dataset, get_distance, eps, min_pts, label_dict)
    cluster_groups = group_by_cluster(label_dict)
    sorted_n_groups = sort_n_groups_by_size(cluster_groups, n)

    output_prefix = input_data_file_name.replace('.txt', '')

    write_clusters(sorted_n_groups, output_prefix)


if __name__ == '__main__':
    main(*sys.argv[1:])
