from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from brick_breaker_env import BrickBreakerEnv  # Импорт вашей среды

# Создаём среду
env = DummyVecEnv([lambda: BrickBreakerEnv()])

# Инициализация модели PPO с использованием GPU (device="cuda")
model = PPO("CnnPolicy", env, device="cuda", verbose=1)

# Начало обучения
TIMESTEPS = 10000  # Количество шагов обучения
model.learn(total_timesteps=TIMESTEPS)

# Сохранение модели
model.save("models/brick_breaker_model")
print("Модель сохранена!")
