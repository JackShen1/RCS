import numpy as np

Y = 0.57
T_RELIABILITY = 1210
T_INTENSITY = 1375
INTERVALS_NUM = 10


def get_input_data(filename: str) -> np.ndarray:
    with open(filename, "r") as f:
        input_data = f.read()
    return np.fromstring(input_data.replace("\n", " "), dtype=int, sep=",")


data = get_input_data("data.txt")
data.sort()

h = data[-1] / INTERVALS_NUM
works_in_interval = [[x for x in data if i * h <= x <= (i + 1) * h] for i in range(INTERVALS_NUM)]
density = np.array([len(sample) / (len(data) * h) for sample in works_in_interval])


def calc_t_y() -> float:
    probs = np.array([1 - density[:i].sum() * h for i in range(INTERVALS_NUM + 1)])
    ti = (probs < Y).argmax()
    d = (probs[ti] - Y) / (probs[ti] - probs[ti - 1])
    return h - h * d


def calc_trouble_free_work_prob(hours: int) -> tuple[float, int]:
    index = (np.array([h * i for i in range(INTERVALS_NUM + 1)]) > hours).argmax() - 1
    return 1 - density[:index].sum() * h - (hours - h * index) * density[index], index


def calc_failure_intensity() -> float:
    intensity, index = calc_trouble_free_work_prob(T_INTENSITY)
    return density[index] / intensity


print(f"\033[1mСередній наробіток до відмови Tср\033[0m: {data.mean()}")
print(f"\033[1mγ-відсотковий наробіток на відмову Tγ при γ = {Y}\033[0m: {calc_t_y()}")
print(f"\033[1mЙмовірність безвідмовної роботи на час {T_RELIABILITY} годин\033[0m: {calc_trouble_free_work_prob(T_RELIABILITY)[0]}")
print(f"\033[1mІнтенсивність відмов на час {T_INTENSITY} годин\033[0m: {calc_failure_intensity()}")
