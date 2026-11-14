import '../models/user.dart';
import 'api_client.dart';

class AuthService {
  final ApiClient _client;

  AuthService(this._client);

  Future<void> register({required String email, required String password, required String fullName}) async {
    await _client.post('/auth/register', {
      'email': email,
      'password': password,
      'full_name': fullName,
    });
  }

  Future<void> login({required String email, required String password}) async {
    final data = await _client.post('/auth/login', {
      'email': email,
      'password': password,
    });
    await _client.saveTokens(
      accessToken: data['access_token'] as String,
      refreshToken: data['refresh_token'] as String,
    );
  }

  Future<AppUser> fetchCurrentUser() async {
    final data = await _client.get('/users/me');
    return AppUser.fromJson(data as Map<String, dynamic>);
  }

  Future<void> logout() async {
    await _client.clearTokens();
  }
}
