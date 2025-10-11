import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------
# 1️⃣  Fungsi Gelombang Hidrogen
# -----------------------------------------------------
def hydrogen_wavefunction(n, l, m, r, theta, phi):
    """Menghitung fungsi gelombang orbital hidrogen Ψ(n,l,m)"""
    a0 = 1.0  # Bohr radius

    # --- Bagian radial (disederhanakan agar bentuknya terlihat jelas) ---
    if n == 1 and l == 0:
        R = 2 * np.exp(-r / a0)
    elif n == 2 and l == 0:
        R = (1 / (2 * np.sqrt(2))) * (2 - r / a0) * np.exp(-r / (2 * a0))
    elif n == 2 and l == 1:
        R = (1 / (2 * np.sqrt(6))) * (r / a0) * np.exp(-r / (2 * a0))
    elif n == 3 and l == 2:
        R = (1 / (81 * np.sqrt(30))) * (r**2 / a0**2) * np.exp(-r / (3 * a0))
    else:
        R = np.exp(-r / a0)  # fallback sederhana

    # --- Fungsi harmonik bola sederhana ---
    if l == 0:
        Y = np.ones_like(theta) / np.sqrt(4 * np.pi)
    elif l == 1 and m == 0:
        Y = np.sqrt(3 / (4 * np.pi)) * np.cos(theta)
    elif l == 1 and m == 1:
        Y = -np.sqrt(3 / (8 * np.pi)) * np.sin(theta) * np.exp(1j * phi)
    elif l == 2 and m == 0:
        Y = np.sqrt(5 / (16 * np.pi)) * (3 * np.cos(theta)**2 - 1)
    elif l == 2 and m == 1:
        Y = -np.sqrt(15 / (8 * np.pi)) * np.sin(theta) * np.cos(theta) * np.exp(1j * phi)
    else:
        Y = np.zeros_like(theta)

    return R * Y


# -----------------------------------------------------
# 2️⃣  Membuat grid 3D
# -----------------------------------------------------
def make_grid(rmax=8, points=70):
    """Membuat grid kartesian dan konversi ke koordinat bola"""
    x = np.linspace(-rmax, rmax, points)
    y = np.linspace(-rmax, rmax, points)
    z = np.linspace(-rmax, rmax, points)
    X, Y, Z = np.meshgrid(x, y, z)
    r = np.sqrt(X**2 + Y**2 + Z**2)
    theta = np.arccos(np.divide(Z, r, out=np.zeros_like(r), where=r != 0))
    phi = np.arctan2(Y, X)
    return r, theta, phi, X, Y, Z


# -----------------------------------------------------
# 3️⃣  Visualisasi Plotly di Streamlit
# -----------------------------------------------------
def visualize_orbital(X, Y, Z, dens, title="Orbital Hidrogen |ψ|²"):
    """Menampilkan visualisasi 3D dari probabilitas densitas elektron"""
    fig = go.Figure(
        data=go.Volume(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=dens.flatten(),
            isomin=np.nanpercentile(dens, 1),
            isomax=np.nanmax(dens),
            opacity=0.25,
            surface_count=25,
            colorscale="Viridis",
        )
    )
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z",
            aspectmode="cube",
        ),
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------
# 4️⃣  Aplikasi Streamlit
# -----------------------------------------------------
st.title("🌀 Visualisasi 3D Orbital Atom Hidrogen")
st.write("By Chantika, Getha, Wijaya")
st.write("Gunakan slider di bawah untuk memilih bilangan kuantum:")

# Slider 3 bilangan kuantum
n = st.slider("Bilangan Kuantum Utama (n)", 1, 5, 2)
l = st.slider("Bilangan Kuantum Azimut (l)", 0, n - 1, 1)

# ✅ Perbaikan penting: hindari error min=max saat l = 0
if l == 0:
    m = 0
    st.write("Bilangan Kuantum Magnetik (m): 0 (karena l = 0)")
else:
    m = st.slider("Bilangan Kuantum Magnetik (m)", -l, l, 0, key=f"m_{l}_{n}")

# -----------------------------------------------------
# 5️⃣  Hitung dan tampilkan hasil
# -----------------------------------------------------
r, theta, phi, X, Y, Z = make_grid(rmax=8, points=60)
psi = hydrogen_wavefunction(n, l, m, r, theta, phi)
dens = np.abs(psi)**2
dens = dens / np.nanmax(dens)
dens = dens ** 0.5  # meningkatkan kontras

# Label jenis orbital otomatis
label_orbital = f"{n}{['s', 'p', 'd', 'f', 'g'][l] if l < 5 else '?'}"

visualize_orbital(X, Y, Z, dens, title=f"Orbital Hidrogen {label_orbital} (n={n}, l={l}, m={m})")

st.success(f"✅ Visualisasi {label_orbital} berhasil ditampilkan!")
