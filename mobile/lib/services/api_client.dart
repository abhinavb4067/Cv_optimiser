import 'dart:convert';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

class ApiException implements Exception {
  final int statusCode;
  final String message;

  ApiException(this.statusCode, this.message);

  @override
  String toString() => message;
}

class ApiClient {
  // Android emulator reaches the host machine's localhost via 10.0.2.2.
  // Override at build time with --dart-define=API_BASE_URL=... for a real device or iOS simulator.
  static const String _defaultBaseUrl = 'http://10.0.2.2:8000/api/v1';
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: _defaultBaseUrl,
  );

  static const _storage = FlutterSecureStorage();
  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';

  Future<String?> get accessToken => _storage.read(key: _accessTokenKey);

  Future<void> saveTokens({required String accessToken, required String refreshToken}) async {
    await _storage.write(key: _accessTokenKey, value: accessToken);
    await _storage.write(key: _refreshTokenKey, value: refreshToken);
  }

  Future<void> clearTokens() async {
    await _storage.delete(key: _accessTokenKey);
    await _storage.delete(key: _refreshTokenKey);
  }

  Future<Map<String, String>> _headers({bool authenticated = false}) async {
    final headers = {'Content-Type': 'application/json'};
    if (authenticated) {
      final token = await accessToken;
      if (token != null) {
        headers['Authorization'] = 'Bearer $token';
      }
    }
    return headers;
  }

  dynamic _decode(http.Response response) {
    final body = response.body.isNotEmpty ? jsonDecode(response.body) : null;
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return body;
    }
    final detail = (body is Map && body['detail'] != null) ? body['detail'].toString() : 'Request failed';
    throw ApiException(response.statusCode, detail);
  }

  Future<dynamic> get(String path, {bool authenticated = true}) async {
    final response = await http.get(
      Uri.parse('$baseUrl$path'),
      headers: await _headers(authenticated: authenticated),
    );
    return _decode(response);
  }

  Future<dynamic> post(String path, Map<String, dynamic> body, {bool authenticated = false}) async {
    final response = await http.post(
      Uri.parse('$baseUrl$path'),
      headers: await _headers(authenticated: authenticated),
      body: jsonEncode(body),
    );
    return _decode(response);
  }
}
