import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.special import sph_harm

st.title("🔬 Visualisasi 3D Orbital Atom Hidrogen")

n = st.slider("Bilangan Kuantum Utama (n)", 1, 5, 2)
l = st.slider("Bilangan Kuantum Azimut (l)", 0, n-1, 1)
m = st.slider("Bilangan Kuantum Magnetik (m)", -l, l, 0)

r = np.linspace(0, 15, 80)
theta = np.linspace(0, np.pi, 80)
phi = np.linspace(0, 2*np.pi, 80)
r, theta, phi = np.meshgrid(r, theta, phi)

R = np.exp(-r/n) * (r/n)**l
Y = sph_harm(m, l, phi, theta)
psi = R * Y
density = np.abs(psi)**2

x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

fig = go.Figure(data=[go.Volume(
    x=x.flatten(), y=y.flatten(), z=z.flatten(),
    value=density.flatten(),
    isomin=density.max()*0.3,
    isomax=density.max(),
    opacity=0.1,
    surface_count=12,
    colorscale='Viridis'
)])
fig.update_layout(scene=dict(aspectmode='cube'))

st.plotly_chart(fig)
