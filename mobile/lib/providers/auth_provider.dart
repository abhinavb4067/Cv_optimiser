import 'package:flutter/foundation.dart';

import '../models/user.dart';
import '../services/api_client.dart';
import '../services/auth_service.dart';

enum AuthStatus { unknown, authenticated, unauthenticated }

class AuthProvider extends ChangeNotifier {
  final ApiClient _client = ApiClient();
  late final AuthService _authService = AuthService(_client);

  AuthStatus status = AuthStatus.unknown;
  AppUser? user;
  String? error;

  Future<void> bootstrap() async {
    final token = await _client.accessToken;
    if (token == null) {
      status = AuthStatus.unauthenticated;
      notifyListeners();
      return;
    }
    try {
      user = await _authService.fetchCurrentUser();
      status = AuthStatus.authenticated;
    } catch (_) {
      await _authService.logout();
      status = AuthStatus.unauthenticated;
    }
    notifyListeners();
  }

  Future<bool> login(String email, String password) async {
    error = null;
    try {
      await _authService.login(email: email, password: password);
      user = await _authService.fetchCurrentUser();
      status = AuthStatus.authenticated;
      notifyListeners();
      return true;
    } catch (e) {
      error = 'Invalid email or password';
      notifyListeners();
      return false;
    }
  }

  Future<bool> register(String email, String password, String fullName) async {
    error = null;
    try {
      await _authService.register(email: email, password: password, fullName: fullName);
      return await login(email, password);
    } catch (e) {
      error = 'Could not create account. The email may already be in use.';
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    user = null;
    status = AuthStatus.unauthenticated;
    notifyListeners();
  }
}
