class AppUser {
  final String id;
  final String email;
  final String? fullName;
  final String role;
  final bool isActive;
  final bool isEmailVerified;

  AppUser({
    required this.id,
    required this.email,
    required this.fullName,
    required this.role,
    required this.isActive,
    required this.isEmailVerified,
  });

  factory AppUser.fromJson(Map<String, dynamic> json) {
    return AppUser(
      id: json['id'] as String,
      email: json['email'] as String,
      fullName: json['full_name'] as String?,
      role: json['role'] as String,
      isActive: json['is_active'] as bool,
      isEmailVerified: json['is_email_verified'] as bool,
    );
  }
}
