{{/*
Expand the name of the chart.
*/}}
{{- define "services.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "services.fullname" -}}
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
{{- define "services.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "services.labels" -}}
{{ include "services.selectorLabels" . }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "services.selectorLabels" -}}
{{- end }}

{{/* 
Proxy config for istio (indent 8)
*/}}
{{- define "services.istioProxyConfig" -}}
readiness.status.sidecar.istio.io/applicationPorts: ""
sidecar.istio.io/inject: "true"
proxy.istio.io/config: |
  tracing:
    zipkin:
      address: zipkin.istio-system:9411
    sampling: 10
    custom_tags:
      http.header.portal:
        header:
          name: portal
      http.header.device:
        header:
          name: device
      http.header.user:
        header:
          name: user
      http.header.travel:
        header:
          name: travel
{{- end }}


{{- define "services.env" -}}
- name: LISTEN_ADDRESS
  value: ":8000"
- name: DISCOUNT_SERVICE
  value: "http://discounts.travel-agency:8000"
- name: MYSQL_SERVICE
  value: "mysqldb.travel-agency:3306"
{{- end }}
  
{{- define "services.mysqlEnv" }}
- name: MYSQL_USER
  value: "root"
- name: MYSQL_PASSWORD
  valueFrom:
    secretKeyRef:
      name: mysql-credentials
      key: rootpasswd
- name: MYSQL_DATABASE
  value: "test"
{{- end }}