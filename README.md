# BirdNET-Pi Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
[![maintainer](https://img.shields.io/badge/maintainer-%40djiesr-blue.svg)](https://github.com/djiesr)
[![fr](https://img.shields.io/badge/lang-fr-yellow.svg)](https://github.com/djiesr/birdnet-ha/blob/main/README.md)

Cette intégration Home Assistant permet de connecter votre instance BirdNET-Pi à Home Assistant, offrant ainsi un suivi en temps réel des détections d'oiseaux et des statistiques.

## Fonctionnalités

- Suivi en temps réel des détections d'oiseaux
- Statistiques quotidiennes des espèces détectées
- Nombre total de détections par jour
- Liste des espèces détectées
- État de connexion au serveur BirdNET-Pi
- Personnalisation de l'intervalle de mise à jour

## Prérequis

- Une instance BirdNET-Pi fonctionnelle (voir [BirdNET-Pi](https://github.com/mcguirepr89/BirdNET-Pi))
- Home Assistant version 2023.8.0 ou supérieure
- HACS (optionnel, mais recommandé pour l'installation)

## Installation

### Méthode 1 : Via HACS (Recommandée)

1. Assurez-vous que [HACS](https://hacs.xyz/) est installé
2. Dans HACS, allez dans "Intégrations"
3. Cliquez sur les trois points en haut à droite
4. Sélectionnez "Dépôts personnalisés"
5. Ajoutez `https://github.com/djiesr/birdnet-ha`
6. Recherchez "BirdNET-Pi" dans HACS
7. Cliquez sur "Télécharger"

### Méthode 2 : Installation manuelle

1. Téléchargez ce dépôt
2. Copiez le dossier `birdnet-pi` dans votre dossier `custom_components`
3. Redémarrez Home Assistant

## Configuration

1. Dans Home Assistant, allez dans "Paramètres" > "Appareils et services"
2. Cliquez sur "Ajouter une intégration"
3. Recherchez "BirdNET-Pi"
4. Entrez l'adresse IP et le port de votre serveur BirdNET-Pi
5. Configurez l'intervalle de mise à jour selon vos besoins

## Entités disponibles

### Capteurs (Sensors)
- Dernières détections
- Nombre total de détections aujourd'hui
- Nombre d'espèces détectées aujourd'hui
- Liste des espèces détectées aujourd'hui
- Statistiques quotidiennes

### Capteurs binaires (Binary Sensors)
- État de connexion au serveur BirdNET-Pi

## Personnalisation

Vous pouvez personnaliser l'intervalle de mise à jour dans les options de l'intégration :
1. Allez dans "Paramètres" > "Appareils et services"
2. Trouvez l'intégration BirdNET-Pi
3. Cliquez sur "Configurer"
4. Ajustez l'intervalle de mise à jour selon vos besoins

## Support

Si vous rencontrez des problèmes ou avez des questions :
- Ouvrez une issue sur GitHub
- Vérifiez que votre serveur BirdNET-Pi est accessible
- Assurez-vous que les ports sont correctement configurés

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer une pull request pour améliorer l'intégration
- Améliorer la documentation

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.