import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:career_assistant_app/providers/auth_provider.dart';
import 'package:career_assistant_app/screens/register_screen.dart';

Widget _wrap(Widget child) {
  return ChangeNotifierProvider(
    create: (_) => AuthProvider(),
    child: MaterialApp(home: child),
  );
}

void main() {
  testWidgets('shows validation errors on empty submit', (tester) async {
    await tester.pumpWidget(_wrap(const RegisterScreen()));

    await tester.tap(find.widgetWithText(FilledButton, 'Create account'));
    await tester.pump();

    expect(find.text('Enter your name'), findsOneWidget);
    expect(find.text('Enter a valid email'), findsOneWidget);
    expect(find.text('At least 8 characters'), findsOneWidget);
  });

  testWidgets('rejects a short password', (tester) async {
    await tester.pumpWidget(_wrap(const RegisterScreen()));

    await tester.enterText(find.widgetWithText(TextFormField, 'Full name'), 'Jane Doe');
    await tester.enterText(find.widgetWithText(TextFormField, 'Email'), 'jane@example.com');
    await tester.enterText(find.widgetWithText(TextFormField, 'Password'), 'short');
    await tester.tap(find.widgetWithText(FilledButton, 'Create account'));
    await tester.pump();

    expect(find.text('At least 8 characters'), findsOneWidget);
  });
}
