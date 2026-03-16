# Déploiement sur NAS (Portainer)

Ce guide explique comment déployer l'app sur un NAS Synology via Portainer,
avec mise à jour automatique à chaque push sur `main`.

---

## Vue d'ensemble

```
GitHub push → CI (tests) → Build image → Push GHCR → Webhook → Portainer pull → Redéploiement
```

- **Registry :** GitHub Container Registry (`ghcr.io/tomboulier/recos-antibioprophylaxie-sfar`)
- **Déclencheur CD :** push sur `main` uniquement
- **Secret requis :** `PORTAINER_WEBHOOK_URL` dans les secrets GitHub

---

## 1. Préparer Portainer sur le NAS

### Créer le stack

1. Ouvrir Portainer → **Stacks** → **Add stack**
2. Nom : `sfar-antibio`
3. Coller le contenu du `docker-compose.yml` (ou pointer sur ce repo via Git)
4. Ajouter les variables d'environnement (voir section `.env` ci-dessous)
5. Cliquer **Deploy the stack**

### Récupérer l'URL du webhook

1. Dans Portainer, ouvrir le stack `sfar-antibio`
2. Aller dans l'onglet **Webhooks**
3. Activer le webhook → copier l'URL générée

---

## 2. Configurer le secret GitHub

1. Sur GitHub → Settings → Secrets and variables → Actions
2. Ajouter le secret : `PORTAINER_WEBHOOK_URL` = l'URL copiée ci-dessus

À chaque push sur `main`, GitHub Actions va :
1. Builder l'image Docker
2. La publier sur GHCR (`ghcr.io/tomboulier/recos-antibioprophylaxie-sfar:latest`)
3. Appeler le webhook Portainer → l'app se redéploie automatiquement

---

## 3. Variables d'environnement (.env)

Créer un fichier `.env` sur le NAS (ou configurer via Portainer UI) :

```env
# Obligatoire pour le chatbot IA (optionnel si vous n'utilisez pas le chat)
MISTRAL_API_KEY=your_api_key_here

# Optionnel
LOG_LEVEL=INFO
```

---

## 4. Exposer l'app à l'extérieur (HTTPS)

### Option A — Nginx Proxy Manager (recommandé si déjà installé)

1. Dans NPM → **Proxy Hosts** → **Add Proxy Host**
2. Domain name : `sfar.votre-domaine.fr`
3. Forward hostname : `sfar-antibio` (ou IP du NAS)
4. Forward port : `8000`
5. Activer **SSL** (Let's Encrypt) + **Force SSL**

### Option B — Synology Reverse Proxy (intégré)

1. Panneau de configuration Synology → **Login Portal** → **Advanced** → **Reverse Proxy**
2. Créer une règle :
   - Source : `https://sfar.votre-domaine.fr:443`
   - Destination : `http://localhost:8000`
3. Configurer le certificat Let's Encrypt dans le gestionnaire de certificats

### Option C — Cloudflare Tunnel (sans ouvrir de port)

```bash
# Installer cloudflared sur le NAS, puis :
cloudflared tunnel --url http://localhost:8000
```

---

## 5. Vérifier le déploiement

```bash
# Santé de l'app
curl http://localhost:8000/api/v1/health

# Logs
docker logs sfar-antibio -f
```

---

## Troubleshooting

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| Image non trouvée | Package GHCR privé | Rendre le package public sur GitHub |
| Webhook timeout | NAS non joignable depuis internet | Vérifier le pare-feu / port forwarding |
| App ne démarre pas | Variable d'env manquante | Vérifier `.env` / variables Portainer |
