# dspace-clip-api / Dossier server

Ce dossier contient des fichiers de configuration pour exécuter un *flow* Jina constitué de deux modules,  clip-as-service et AnnLite.

La description de chaque configuration se trouve en commentaires dans les fichiers.

## Dépendances

Les modules clip_server et annlite doivent être installés dans votre environnement Python:

```sh
pip install clip_server
pip install annlite
```

Ensuite, pour démarrer le serveur:

```sh
python -m clip_server [fichier flow]
```

Le dossier `server` contient des exemples de fichiers *flow*. En particulier, le fichier `flow_standard.yml` devrait fonctionner pour une configuration de base.

Si tout fonctionne bien, vous devriez obtenir quelque chose comme ceci dans votre console:

```
───────────────────────────────────────────────────────────────────────────── 🎉 Flow is ready to serve! ─────────────────────────────────────────────────────────────────────────────
╭────────────── 🔗 Endpoint ───────────────╮
│  ⛓      Protocol                   GRPC  │
│  🏠        Local          0.0.0.0:51000  │
│  🔒      Private       10.0.0.248:51000  │
│  🌍       Public     96.22.88.174:51000  │
│  ⛓      Protocol                   HTTP  │
│  🏠        Local          0.0.0.0:54322  │
│  🔒      Private       10.0.0.248:54322  │
│  🌍       Public     96.22.88.174:54322  │
│  ⛓      Protocol              WEBSOCKET  │
│  🏠        Local          0.0.0.0:54323  │
│  🔒      Private       10.0.0.248:54323  │
│  🌍       Public     96.22.88.174:54323  │
╰──────────────────────────────────────────╯
╭─────────── 💎 HTTP extension ────────────╮
│  💬    Swagger UI    0.0.0.0:54322/docs  │
│  📚         Redoc   0.0.0.0:54322/redoc  │
```
