apiVersion: apps/v1
kind: Deployment
metadata:
  name: ultimanager-api
  labels:
    app: ultimanager-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ultimanager-api
  template:
    metadata:
      labels:
        app: ultimanager-api
    spec:
      containers:
        - name: ultimanager-api
          image: @IMAGE_REPO@/@IMAGE_NAME@:@IMAGE_TAG@
          env:
            - name: SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: api-secret-key
                  key: SECRET_KEY

            - name: ALLOWED_HOSTS
              valueFrom:
                configMapKeyRef:
                  name: domains-config
                  key: API_DOMAIN

            - name: DB_TYPE
              value: postgres

            - name: DB_HOST
              valueFrom:
                secretKeyRef:
                  name: db-creds
                  key: host

            - name: DB_NAME
              value: ultimanager_api

            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-creds
                  key: password

            - name: DB_PORT
              valueFrom:
                secretKeyRef:
                  name: db-creds
                  key: port

            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: db-creds
                  key: username

            - name: IS_HTTPS
              value: "True"

          ports:
            - containerPort: 8000
              name: http

          resources:
            requests:
              cpu: 50m
              memory: 50Mi

            limits:
              memory: 200Mi
