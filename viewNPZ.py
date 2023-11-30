from numpy import load

data = load('ImageLogs/models/ppo_default2/best/evaluations.npz')
lst = data.files
for item in lst:
    print(item)
    print(data[item])