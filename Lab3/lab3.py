from math import log, factorial

from Lab2.lab2 import P_system, probs, working_states, get_probs

TIME = 2501
K = 3


def find_t_system(prob: float) -> float:
    return (-1 * TIME) / log(prob)


Q_system = 1 - P_system
T_system = find_t_system(prob=P_system)
print(f"\033[1mЙмовірність безвідмовної роботи на час {TIME} годин:\033[0m {P_system:.6f}\n"
      f"\033[1mЙмовірність відмови на час {TIME} годин:\033[0m {Q_system:.6f}\n"
      f"\033[1mСередній наробіток до відмови системи без резервування:\033[0m {T_system:.2f} годин\n")

Q_res_system = Q_system / factorial(K + 1)
print(f"\033[1mЙмовірність відмови на час {TIME} годин системи з загальним ненавантаженим "
      f"резервуванням з кратністю {K}:\033[0m {Q_res_system:.6f}")

P_res_system = 1 - Q_res_system
print(f"\033[1mЙмовірність безвідмовної роботи на час {TIME} годин системи з загальним ненавантаженим "
      f"резервуванням:\033[0m {P_res_system:.6f}")

T_res_system = find_t_system(prob=P_res_system)
print(f"\033[1mСередній наробіток до відмови системи з загальним ненавантаженим "
      f"резервуванням:\033[0m {T_res_system:.2f}\n")

_system = (Q_system, P_system, T_system)
_res_system = (Q_res_system, P_res_system, T_res_system)

G_sys = [_res_system[i] / _system[i] for i, _ in enumerate(_system)]
print(f"\033[1mВиграш надійності протягом часу {TIME} годин за ймовірністю відмов:\033[0m {G_sys[0]:.2f}\n"
      f"\033[1mВиграш надійності протягом часу {TIME} годин за ймовірністю безвідмовної роботи:\033[0m {G_sys[1]:.2f}\n"
      f"\033[1mВиграш надійності за середнім часом безвідмовної роботи:\033[0m {G_sys[2]:.2f}\n")

Q_t = [pow(1 - p, K + 1) for p in probs]
P_t = [1 - q for q in Q_t]
print(f"\033[1mЙмовірність відмови та безвідмовної роботи кожного елемента системи при його "
      f"навантаженому резервуванні з кратністю {K}:\033[0m")
print('-' * 51)
for i, elems in enumerate(zip(Q_t[1:-1], P_t[1:-1])):
    print("|" + f"Q_reserved{i+1} = {elems[0]:.5f}".center(24) +
          "|" + f"P_reserved{i+1} = {elems[1]:.5f}".center(24) + "|")
print('-' * 51)

probabilities = get_probs(all_working_states=working_states, probs=P_t)

P_res_system2 = sum(probabilities)
Q_res_system2 = 1 - P_res_system2
T_res_system2 = find_t_system(prob=P_res_system2)
print(f"\033[1mЙмовірність безвідмовної роботи  системи в цілому:\033[0m {P_res_system2:.6f}\n"
      f"\033[1mЙмовірність відмови системи в цілому\033[0m {Q_res_system2:.6f}\n"
      f"\033[1mСередній наробіток системи в цілому:\033[0m {T_res_system2:.2f} годин\n")

_res_system2 = (Q_res_system2, P_res_system2, T_res_system2)
G_sys2 = [_res_system2[i] / _system[i] for i, _ in enumerate(_system)]
print(f"\033[1mВиграш надійності за ймовірністю відмов:\033[0m {G_sys2[0]:.2f}\n"
      f"\033[1mВиграш надійності за ймовірністю безвідмовної роботи:\033[0m {G_sys2[1]:.2f}\n"
      f"\033[1mВиграш надійності за середнім часом безвідмовної роботи:\033[0m {G_sys2[2]:.2f}")
