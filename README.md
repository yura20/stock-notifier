# Stock Notifier

This project sends **stock price variation alerts** using a Python script running as a **Kubernetes CronJob**. Notifications are sent via [ntfy.sh](https://ntfy.sh).

## Features

- Configurable **STOCK_CODE** and **TOPIC** via environment variables.
- Optional **VARIATION_STARTWITH**: send alerts only when variation starts with a specific character (e.g., "-", "+").
- Runs on **weekdays, every hour from 9 AM to 5 PM by Paris Time**.
- Fully containerized using Docker.
- Deployable in **Kubernetes** with ConfigMaps for environment configuration.


## Deploy to Kubernetes (using Kustomize)
```bash
kubectl apply -k k8s/base/
```

## Verify CronJob
```bash
kubectl create job --from=cronjob/stock-notifier-cron stock-notifier-test -n stocks
```

## Environment Variables (via ConfigMap)

- `TOPIC` – Ntfy.sh topic to send notifications to.
- `STOCK_CODE` – Stock or index code to scrape.
- `VARIATION_STARTWITH` – Optional. Only send alerts if the value starts with this character.