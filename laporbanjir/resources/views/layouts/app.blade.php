<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'LaporBanjir - BPBD Kab. Bandung')</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background-color: #f8fafc;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .main-container {
            flex: 1;
        }
        .badge-menunggu { background-color: #f59e0b; color: white; }
        .badge-diproses { background-color: #3b82f6; color: white; }
        .badge-selesai { background-color: #10b981; color: white; }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4">
        <div class="container">
            <a class="navbar-brand fw-bold" href="{{ route('laporans.create') }}">
                <i class="fas fa-water me-2"></i>LaporBanjir BPBD
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link {{ request()->routeIs('laporans.create') ? 'active fw-bold' : '' }}" href="{{ route('laporans.create') }}">
                            <i class="fas fa-bullhorn me-1"></i>Form Pengaduan
                        </a>
                    </li>
                    @auth
                    <li class="nav-item">
                        <a class="nav-link {{ request()->routeIs('laporans.index') ? 'active fw-bold' : '' }}" href="{{ route('laporans.index') }}">
                            <i class="fas fa-clipboard-list me-1"></i>Kelola Laporan
                        </a>
                    </li>
                    @endauth
                </ul>
                <ul class="navbar-nav ms-auto align-items-center">
                    @auth
                    <li class="nav-item me-2">
                        <span class="nav-link text-white">
                            <i class="fas fa-user-shield me-1"></i>Petugas: <strong>{{ Auth::user()->name }}</strong>
                        </span>
                    </li>
                    <li class="nav-item">
                        <form action="{{ route('logout') }}" method="POST" class="d-inline">
                            @csrf
                            <button type="submit" class="btn btn-sm btn-light text-primary fw-semibold">
                                <i class="fas fa-sign-out-alt me-1"></i>Logout
                            </button>
                        </form>
                    </li>
                    @else
                    <li class="nav-item">
                        <a class="nav-link {{ request()->routeIs('login') ? 'active' : '' }}" href="{{ route('login') }}">
                            <i class="fas fa-sign-in-alt me-1"></i>Login Petugas
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {{ request()->routeIs('register') ? 'active' : '' }}" href="{{ route('register') }}">
                            <i class="fas fa-user-plus me-1"></i>Register
                        </a>
                    </li>
                    @endauth
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content Container -->
    <div class="container main-container">
        @if (session('success'))
            <div class="alert alert-success alert-dismissible fade show shadow-sm" role="alert">
                <i class="fas fa-check-circle me-2"></i>{{ session('success') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif

        @if ($errors->any())
            <div class="alert alert-danger alert-dismissible fade show shadow-sm" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i><strong>Ada kesalahan input:</strong> Silakan periksa kembali form di bawah ini.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif

        @yield('content')
    </div>

    <!-- Footer -->
    <footer class="bg-white border-top text-center py-3 mt-5 text-muted small">
        <div class="container">
            &copy; 2026 BPBD Kabupaten Bandung &bull; Sistem Informasi Siaga & Lapor Banjir (Praktikum PABW Modul 7)
        </div>
    </footer>

    <!-- Bootstrap Bundle JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
