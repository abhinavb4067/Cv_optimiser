import '../models/dashboard_summary.dart';
import 'api_client.dart';

class DashboardService {
  final ApiClient _client;

  DashboardService(this._client);

  Future<DashboardSummary> fetchSummary() async {
    final data = await _client.get('/dashboard/summary');
    return DashboardSummary.fromJson(data as Map<String, dynamic>);
  }
}
