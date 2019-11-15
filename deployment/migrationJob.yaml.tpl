apiVersion: batch/v1
kind: Job
metadata:
  # Name has to be under 63 characters with a 40 character hash
  name: ulti-api-m-@IMAGE_TAG@
spec:
  template:
    spec:
      containers:
        - name: ultimanager-api
          image: @IMAGE_REPO@/@IMAGE_NAME@:@IMAGE_TAG@

          args: ['migrate']

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
      restartPolicy: Never
  backoffLimit: 4
