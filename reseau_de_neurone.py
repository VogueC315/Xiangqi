from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from Environnement_IA import XiangqiEnv
from xiangqi_cnn import XiangqiCNN

# 1. Créer l'environnement
env = XiangqiEnv()

# 2. Vérifier que l'environnement respecte bien l'API Gymnasium
check_env(env, warn=True)

# 3. Créer le modèle PPO en utilisant une policy adaptée aux entrées de type image (tenseur multi-canal)
policy_kwargs = dict(features_extractor_class=XiangqiCNN,features_extractor_kwargs=dict(features_dim=256),)

model = PPO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1)



# 4. Entraîner l'agent pendant 100000 timesteps (ajuste ce nombre selon tes ressources)
model.learn(total_timesteps=100)

# 5. Sauvegarder le modèle entraîné
model.save("ppo_xiangqi_model")

# 6. Boucle d'évaluation
obs, _ = env.reset()
done = False
while not done:
    # L'agent prédit l'action à effectuer
    action, _states = model.predict(obs)
    obs, reward, done, truncated, info = env.step(action)
    env.render()

env.close()
