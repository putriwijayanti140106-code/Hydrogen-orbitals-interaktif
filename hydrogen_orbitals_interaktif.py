import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------
# 1️⃣  Fungsi matematika orbital hidrogen
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
# 3️⃣  Visualisasi Plotly
# -----------------------------------------------------
def visualize_orbital(X, Y, Z, dens, title="Orbital Hidrogen |ψ|²"):
    """Menampilkan visualisasi 3D dari probabilitas densitas elektron"""
    fig = go.Figure(
        data=go.Volume(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=dens.flatten(),
            isomin=np.nanpercentile(dens, 1),   # tampilkan lebih banyak area
            isomax=np.nanmax(dens),
            opacity=0.25,                       # transparansi agar struktur dalam terlihat
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
    fig.show()


# -----------------------------------------------------
# 4️⃣  Program utama interaktif
# -----------------------------------------------------
def main():
    print("=== Visualisasi Orbital Hidrogen Interaktif ===")
    print("Contoh nilai:")
    print("  1s → n=1, l=0, m=0")
    print("  2s → n=2, l=0, m=0")
    print("  2p → n=2, l=1, m=0")
    print("  3d → n=3, l=2, m=1")
    print("===============================================")

    try:
        n = int(input("Masukkan n (1–3): "))
        l = int(input("Masukkan l (0–2): "))
        m = int(input("Masukkan m (-l sampai l): "))
    except:
        print("Input tidak valid! Menggunakan nilai default (2,2,0).")
        n, l, m = 2, 2, 0

    print("Menghitung fungsi gelombang...")
    r, theta, phi, X, Y, Z = make_grid(rmax=8, points=60)
    psi = hydrogen_wavefunction(n, l, m, r, theta, phi)
    dens = np.abs(psi)**2

    # Normalisasi dan perkuat nilai supaya terlihat
    dens = dens / np.nanmax(dens)
    dens = dens ** 0.5  # meningkatkan kontras visual

    print("Menampilkan visualisasi interaktif...")
    visualize_orbital(X, Y, Z, dens, title=f"Orbital Hidrogen (n={n}, l={l}, m={m})")


# -----------------------------------------------------
# 5️⃣  Jalankan program
# -----------------------------------------------------
if __name__ == "__main__":
    main()

import webbrowser
import os

def visualize_orbital(X, Y, Z, dens, title="Orbital Hidrogen |ψ|²"):
    ...
    fig.show()
    fig.write_html("orbital_visualization.html")

    # 🌐 buka file HTML hasil render langsung di browser default
    file_path = os.path.abspath("orbital_visualization.html")
    webbrowser.open(filename="orbital_visualization.html")
    print("✅ File visualisasi dibuka otomatis di browser.")
