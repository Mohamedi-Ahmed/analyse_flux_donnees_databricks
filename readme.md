
# Veille et Mise en Pratique - Spark Structured Streaming avec Event Hubs et Kafka

## 1. Veille Technique

### 1.1 Spark Structured Streaming
- Spark Structured Streaming est une API qui permet de traiter des flux de données en temps réel.
- Utilise un **modèle de micro-batchs** ou **traitement continu** pour analyser les données en streaming.
- Intègre des fonctionnalités comme les **fenêtres temporelles**, **checkpointing**, et **gestion des états**.

### 1.2 Azure Event Hubs vs Apache Kafka
| Critère          | Azure Event Hubs  | Apache Kafka |
|-----------------|------------------|-------------|
| **Scalabilité** | Haute (intégration avec Azure) | Très élevée |
| **Facilité d'intégration** | Facile avec Azure Databricks | Requiert une configuration avancée |
| **Latence** | Très faible | Très faible |
| **Tolérance aux pannes** | Automatique (Azure) | Géré avec Zookeeper |
| **Cas d'usage** | IoT, logs, surveillance cloud | Big Data, Analytics, logs volumineux |

## 2. Implémentation

### 2.1 Streaming avec Azure Databricks
- Chargement de fichiers JSON en streaming depuis un stockage Azure.
- Application de transformations sur les données en temps réel.
- Stockage dans **Delta Lake** pour un suivi historique et une analyse améliorée.

### 2.2 Intégration avec Azure Event Hubs
- Utilisation d'**Event Hubs** pour récupérer les données des capteurs IoT en direct.
- Transformation des données et écriture dans **Delta Tables**.

### 2.3 Intégration avec Apache Kafka
- Lecture des données depuis un **topic Kafka**.
- Transformation et écriture vers un autre **topic Kafka** pour analyse en temps réel.

## 3. Comparaison des solutions

| Solution | Avantages | Inconvénients |
|----------|----------|--------------|
| **Azure Event Hubs** | Facilité d'intégration avec Azure, haute scalabilité | Coût élevé sur gros volumes |
| **Apache Kafka** | Open-source, très performant sur le Big Data | Configuration plus complexe |

📌 **Recommandation** :  
- **Si l’infrastructure est sur Azure** → Utiliser **Event Hubs**.  
- **Si besoin d’une flexibilité et d’une architecture hybride** → Privilégier **Kafka**.
