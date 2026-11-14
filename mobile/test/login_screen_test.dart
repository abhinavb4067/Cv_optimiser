import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:career_assistant_app/providers/auth_provider.dart';
import 'package:career_assistant_app/screens/login_screen.dart';

Widget _wrap(Widget child) {
  return ChangeNotifierProvider(
    create: (_) => AuthProvider(),
    child: MaterialApp(home: child),
  );
}

void main() {
  testWidgets('shows validation errors on empty submit', (tester) async {
    await tester.pumpWidget(_wrap(const LoginScreen()));

    await tester.tap(find.text('Sign in'));
    await tester.pump();

    expect(find.text('Enter a valid email'), findsOneWidget);
    expect(find.text('Enter your password'), findsOneWidget);
  });

  testWidgets('rejects an email missing the @ sign', (tester) async {
    await tester.pumpWidget(_wrap(const LoginScreen()));

    await tester.enterText(find.widgetWithText(TextFormField, 'Email'), 'not-an-email');
    await tester.enterText(find.widgetWithText(TextFormField, 'Password'), 'password123');
    await tester.tap(find.text('Sign in'));
    await tester.pump();

    expect(find.text('Enter a valid email'), findsOneWidget);
  });

  testWidgets('navigates to Register screen', (tester) async {
    await tester.pumpWidget(_wrap(const LoginScreen()));

    await tester.tap(find.text("Don't have an account? Register"));
    await tester.pumpAndSettle();

    expect(find.text('Create account'), findsWidgets);
  });
}
