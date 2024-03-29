{{/*
Expand the name of the chart.
*/}}
{{- define "travel-control.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "travel-control.fullname" -}}
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
{{- define "travel-control.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "travel-control.labels" -}}
helm.sh/chart: {{ include "travel-control.chart" . }}
{{ include "travel-control.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "travel-control.selectorLabels" -}}
app.kubernetes.io/name: {{ include "travel-control.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "travel-control.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "travel-control.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "travel-control.rolloutRestart" }}
#!/bin/bash

RUNNING=2
for apps in control;  do
    NS=travel-control
    COUNT=$(oc get pods -l app=${apps} --no-headers -n ${NS} | awk '{print $2}' | awk -F/ '{print $1}')
  while [[ ${COUNT} != 2 ]]; do
    sleep 5
    echo "restarting deployment rollout for ${apps} in ${NS}"
    echo "Running: kubectl rollout restart deploy -l app=${apps} -n ${NS}"
    kubectl rollout restart deploy -l app=${apps} -n ${NS}
    sleep 5
    COUNT=$(oc get pods -l app=${apps} --no-headers -n ${NS} | awk '{print $2}' | awk -F/ '{print $1}')
    done
    echo "done"

  echo "All Set, no restart required in ${NS}"
done
{{- end }}
