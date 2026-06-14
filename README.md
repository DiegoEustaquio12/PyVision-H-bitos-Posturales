#  PyVision: Corrección de Postura Inteligente
> **Tu asistente personal de ergonomía basado en Visión por Computadora.** 🚀

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-OpenCV-green.svg?style=for-the-badge&logo=google&logoColor=white)](https://google.github.io/mediapipe/)
[![PySide6](https://img.shields.io/badge/UI-PySide6%20%2F%20Qt-darkneon.svg?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![ODS 3](https://img.shields.io/badge/ODS%203-Salud%20%26%20Bienestar-emerald.svg?style=for-the-badge)](https://sdgs.un.org/goals/goal3)

---

## 📌 Resumen del Proyecto

**PyVision** es un sistema de software no invasivo diseñado para combatir los riesgos ergonómicos derivados de las largas jornadas frente al ordenador (habitualmente entre 8 y 10 horas diarias). Mediante el uso de una cámara web estándar y técnicas avanzadas de **visión por computadora**, PyVision analiza la alineación corporal del usuario en tiempo real. 

A diferencia de los costosos muebles ergonómicos o los incómodos correctores físicos, PyVision evalúa la postura de manera discreta y, al detectar anomalías sostenidas (como el encorvamiento o el "cuello de texto"), emite notificaciones inteligentes que no interrumpen el flujo de trabajo. El objetivo principal es **reentrenar la memoria muscular** y fomentar hábitos saludables a largo plazo.

---

## 🎨 Interfaz de Usuario (Preview)

El sistema cuenta con un moderno dashboard oscuro diseñado en **PySide** que integra todas las herramientas necesarias para equilibrar salud y productividad:

* **Sesión de Enfoque:** Gestión del tiempo inspirada en la técnica Pomodoro con intervalos de trabajo configurables.
* **Monitoreo en Tiempo Real:** Visualización de la malla de puntos clave (MediaPipe) sobre el feed de la cámara.
* **Gestión de Objetivos:** Metas personalizadas a corto plazo con temporizadores y métricas de cumplimiento.
* **Preferencias:** Control de alertas sonoras, notificaciones en pantalla y calibración de sensibilidad de postura.

---


## 📊 Problemática y Justificación Ergonómica

En México, entre el **25% y el 30% de la población ocupada** trabaja frente a una computadora, mientras que más del **85% de los estudiantes universitarios** la utilizan entre 4 y 5 horas diarias sin hábitos posturales adecuados. 

Estudios demuestran que los factores de riesgo ergonómico se distribuyen drásticamente en la tensión física diaria:
* **Postura:** 50% del impacto total de riesgo.
* **Duración:** 33% debido al tiempo prolongado de exposición.
* **Fuerza / Frecuencia:** 17% restante.

Esta acumulación de estrés físico no solo genera dolor crónico en cuello y columna, sino que reduce la concentración, eleva el estrés y disminuye directamente el rendimiento cognitivo y la productividad.

---

## 🇺🇳 Alineación con los Objetivos de Desarrollo Sostenible (ODS)

PyVision está directamente vinculado con el **ODS 3: Salud y Bienestar** de la ONU, atacando problemáticas de salud física y mental en entornos académicos y profesionales:

| Meta ONU | Descripción ODS | Vínculo Directo con PyVision |
| :---: | :--- | :--- |
| **3.4** | Reducir la mortalidad prematura y promover la salud mental y el bienestar. | Combate el estrés académico, la fatiga y la ansiedad mediante recordatorios de descanso activo y pausas de estiramiento. |
| **3.d** | Reforzar la alerta temprana y la reducción de riesgos para la salud a nivel global. | Actúa como un monitor preventivo que detecta posturas de riesgo físico en tiempo real *antes* de que se conviertan en lesiones crónicas o microlesiones de columna. |

---

## 🚀 Características Principales

* **Detección No Invasiva:** Cero sensores corporales. Solo requiere una cámara web estándar (integrada o externa).
* **Alertas Inteligentes:** Notificaciones diseñadas para avisar únicamente cuando la mala postura es *sostenida*, evitando falsos positivos por movimientos naturales.
* **Pausas Activas y Ergonómicas:** Al terminar los bloques de enfoque, el software sugiere ejercicios correctivos y consejos posturales personalizados.
* **Dashboard de Progreso:** Analíticas e historial de postura para observar la evolución y mejora de los hábitos a lo largo del tiempo.

---

## 💻 Requisitos del Sistema

### Hardware Mínimo
* **Sistema Operativo:** Windows 10 / 11 de 64 bits.
* **Procesador:** CPU Multi-core con soporte para operaciones matriciales.
* **Memoria RAM:** 4 GB (Mínimo).
* **Almacenamiento:** 10 GB de espacio libre.
* **Cámara:** Webcam estándar con resolución mínima de 720p.

### Stack Tecnológico (Software)
* **Lenguaje:** Python 3.10+
* **Visión Artificial:** OpenCV (Procesamiento de imagen) & MediaPipe (Detección de *landmarks* anatómicos).
* **Interfaz Gráfica:** PySide6 (Qt para Python).
* **Control de Versiones:** Git.

---

## 👥 Desarrolladores (BUAP)

Este proyecto es desarrollado de forma colaborativa en la **Facultad de Ciencias de la Computación** de la **Benemérita Universidad Autónoma de Puebla** (Licenciatura en Ingeniería en Ciencias de la Computación):

* **Diego Barbosa R.**
* **Eustaquio Arriaga D. A.**
* **Santos Márquez J.**
* **Torres González M.**

---
*Facultad de Ciencias de la Computación, BUAP — Mayo 2026*