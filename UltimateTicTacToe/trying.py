import numpy as np

arr = np.array([435, 334,  69, 210, 100, 220, 241, 377, 184])
arr2 = np.array([ 76, 177, 442, 301, 411, 291, 270, 134, 326])

valid_actions = np.array(
                arr | arr2
            )

print(valid_actions)