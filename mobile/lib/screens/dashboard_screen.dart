import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/dashboard_summary.dart';
import '../providers/auth_provider.dart';
import '../services/api_client.dart';
import '../services/dashboard_service.dart';
import '../widgets/stat_card.dart';

const _navItems = <_NavItem>[
  _NavItem('Dashboard', Icons.dashboard_outlined),
  _NavItem('My Resumes', Icons.description_outlined),
  _NavItem('AI Resume Builder', Icons.auto_fix_high_outlined),
  _NavItem('ATS Resume Scanner', Icons.fact_check_outlined),
  _NavItem('Job Recommendations', Icons.work_outline),
  _NavItem('Skill Gap Analysis', Icons.insights_outlined),
  _NavItem('Career Roadmap', Icons.map_outlined),
  _NavItem('AI Mock Interviews', Icons.mic_none_outlined),
  _NavItem('Cover Letter Generator', Icons.mail_outline),
  _NavItem('LinkedIn Optimizer', Icons.business_center_outlined),
  _NavItem('Portfolio Builder', Icons.language_outlined),
  _NavItem('Job Application Tracker', Icons.track_changes_outlined),
  _NavItem('Career & Salary Insights', Icons.payments_outlined),
  _NavItem('Subscription & Billing', Icons.credit_card_outlined),
  _NavItem('Settings', Icons.settings_outlined),
];

class _NavItem {
  final String label;
  final IconData icon;
  const _NavItem(this.label, this.icon);
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  late final DashboardService _dashboardService = DashboardService(ApiClient());
  DashboardSummary? _summary;
  int _selectedIndex = 0;

  @override
  void initState() {
    super.initState();
    _loadSummary();
  }

  Future<void> _loadSummary() async {
    try {
      final summary = await _dashboardService.fetchSummary();
      if (mounted) setState(() => _summary = summary);
    } catch (_) {
      // Non-fatal: dashboard just shows an empty state until retried.
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final user = auth.user;

    return Scaffold(
      appBar: AppBar(title: Text(_navItems[_selectedIndex].label)),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(color: Theme.of(context).colorScheme.primaryContainer),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    user?.fullName ?? user?.email ?? '',
                    style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
                  ),
                  Text(user?.role ?? '', style: const TextStyle(fontSize: 12)),
                ],
              ),
            ),
            for (var i = 0; i < _navItems.length; i++)
              ListTile(
                leading: Icon(_navItems[i].icon),
                title: Text(_navItems[i].label),
                selected: i == _selectedIndex,
                onTap: () {
                  setState(() => _selectedIndex = i);
                  Navigator.of(context).pop();
                },
              ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('Log out'),
              onTap: () => context.read<AuthProvider>().logout(),
            ),
          ],
        ),
      ),
      body: _selectedIndex == 0 ? _buildHome(user?.fullName ?? user?.email ?? '') : _buildPlaceholder(),
    );
  }

  Widget _buildHome(String name) {
    final summary = _summary;
    return RefreshIndicator(
      onRefresh: _loadSummary,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Welcome, $name', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          if (summary == null)
            const Padding(
              padding: EdgeInsets.symmetric(vertical: 32),
              child: Center(child: CircularProgressIndicator()),
            )
          else
            GridView.count(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              crossAxisCount: 2,
              mainAxisSpacing: 12,
              crossAxisSpacing: 12,
              childAspectRatio: 1.4,
              children: [
                StatCard(label: 'Uploaded Resumes', value: '${summary.totalUploadedResumes}'),
                StatCard(label: 'Generated Resumes', value: '${summary.totalGeneratedResumes}'),
                StatCard(label: 'Saved Jobs', value: '${summary.savedJobs}'),
                StatCard(label: 'Upcoming Interviews', value: '${summary.upcomingInterviews}'),
                StatCard(label: 'AI Credits', value: '${summary.remainingAiCredits}'),
                StatCard(label: 'Plan', value: summary.subscriptionPlan ?? 'Free'),
              ],
            ),
        ],
      ),
    );
  }

  Widget _buildPlaceholder() {
    return Center(
      child: Text(
        '${_navItems[_selectedIndex].label} is coming in a later phase.',
        style: const TextStyle(color: Colors.grey),
      ),
    );
  }
}
