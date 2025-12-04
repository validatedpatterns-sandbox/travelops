{{- define "otc.config" -}}
config: |
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318
    zipkin:
      endpoint: 0.0.0.0:9411
  exporters:
    debug:
      verbosity: basic
    otlp:
      auth:
        authenticator: bearertokenauth
      endpoint: tempo-tempostack-gateway.tempo.svc.cluster.local:8090
      headers:
        X-Scope-OrgID: dev
      tls:
        ca_file: /var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt
        insecure: false
  processors:
    batch:
      send_batch_size: 1024
      timeout: 1s
  extensions:
    bearertokenauth:
      filename: /var/run/secrets/kubernetes.io/serviceaccount/token
  service:
    extensions:
      - bearertokenauth
    telemetry:
      metrics:
        level: detailed
        readers:
          - pull:
              exporter:
                prometheus:
                  host: 0.0.0.0
                  port: 8888
    pipelines:
      traces:
        exporters:
          - otlp
          - debug
        receivers:
          - otlp
          - zipkin
{{- end }}
