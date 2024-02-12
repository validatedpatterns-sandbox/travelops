{{/*
Expand the name of the chart.
*/}}
{{- define "servicemesh.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "servicemesh.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "servicemesh.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "servicemesh.labels" -}}
helm.sh/chart: {{ include "servicemesh.chart" . }}
{{ include "servicemesh.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "servicemesh.selectorLabels" -}}
app.kubernetes.io/name: {{ include "servicemesh.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "servicemesh.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "servicemesh.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
We are defining various components of the servicemesh controlplane spec. Including 
addons, gateways and runtime configurations. 
*/}}
{{- define "servicemesh.gateways" }}
gateways:
  egress:
    enabled: {{ .Values.gateways.egress.enabled }}
    runtime:
      deployment:
        autoScaling:
          enabled: {{ .Values.gateways.egress.autoscaling.enabled }}
          maxReplicas: {{ .Values.gateways.egress.autoscaling.maxReplicas }}
          minReplicas: {{ .Values.gateways.egress.autoscaling.minReplicas }}
      pod: {}
    service: {}
  enabled: {{ .Values.gateways.enabled }}
  ingress:
    enabled: {{ .Values.gateways.ingress.enabled }}
    runtime:
      deployment:
        autoScaling:
          enabled: {{ .Values.gateways.ingress.autoscaling.enabled }}
          maxReplicas: {{ .Values.gateways.ingress.autoscaling.maxReplicas }}
          minReplicas: {{ .Values.gateways.ingress.autoscaling.minReplicas }}
      pod: {}
    service: {}
  openshiftRoute:
    enabled: {{ .Values.gateways.openshiftRoute.enabled }}
{{- end }}

{{- define "servicemesh.addons" }}
grafana:
  enabled: {{ .Values.grafana.enabled }}
  install:
    config:
      env: {}
      envSecrets: {}
    persistence:
      enabled: {{ .Values.grafana.persistence.enabled }}
      storageClassName: {{ .Values.grafana.persistence.storageClassName | quote }}
      accessMode: {{ .Values.grafana.persistence.accessMode }}
      capacity:
        requests:
          storage: {{ .Values.grafana.persistence.capacity.requests.storage }}
    service:
      ingress:
        contextPath: /grafana
        tls:
          termination: {{ .Values.grafana.service.ingress.tls.termination }} 
jaeger:
  name: jaeger-{{ .Values.global.jaeger.strategy }}
  install:
    ingress:
      enabled: true
    storage:
      type: {{ .Values.jaeger.storage }}
kiali:
  enabled: true
prometheus:
  enabled: true
{{- end }}

{{- define "servicemesh.runtime" }}
components:
  pilot:
    deployment:
      replicas: {{ .Values.pilot.deployment.replicas }}
    pod:
      affinity: {}
    container: {}
  grafana:
    deployment: {}
    pod: {}
  kiali:
    deployment: {}
    pod: {}
{{- end }}
