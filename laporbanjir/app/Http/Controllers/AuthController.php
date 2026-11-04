<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class AuthController extends Controller
{
    /**
     * Menampilkan form register petugas
     */
    public function showRegister(): View
    {
        return view('auth.register');
    }

    /**
     * Memvalidasi data, membuat akun petugas baru, lalu login
     */
    public function register(Request $request): RedirectResponse
    {
        $validated = $request->validate([
            'name'     => 'required|string|max:255',
            'email'    => 'required|string|email|max:255|unique:users,email',
            'password' => 'required|string|min:8|confirmed',
        ]);

        $user = User::create($validated);
        Auth::login($user);
        $request->session()->regenerate();

        return redirect()->route('laporans.index')->with('success', 'Registrasi berhasil, selamat datang Petugas ' . $user->name . '.');
    }

    /**
     * Menampilkan form login petugas
     */
    public function showLogin(): View
    {
        return view('auth.login');
    }

    /**
     * Memeriksa kredensial petugas dan membuat session login
     */
    public function login(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email'    => 'required|string|email',
            'password' => 'required|string',
        ]);

        if (Auth::attempt($credentials, $request->boolean('remember'))) {
            $request->session()->regenerate();
            return redirect()->intended(route('laporans.index'))->with('success', 'Login berhasil. Selamat datang kembali!');
        }

        return back()
            ->withErrors(['email' => 'Email atau password salah.'])
            ->onlyInput('email');
    }

    /**
     * Mengakhiri session login
     */
    public function logout(Request $request): RedirectResponse
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect()->route('login')->with('success', 'Anda berhasil logout.');
    }
}
