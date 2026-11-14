class DashboardSummary {
  final int totalUploadedResumes;
  final int totalGeneratedResumes;
  final int savedJobs;
  final int upcomingInterviews;
  final String? subscriptionPlan;
  final int remainingAiCredits;

  DashboardSummary({
    required this.totalUploadedResumes,
    required this.totalGeneratedResumes,
    required this.savedJobs,
    required this.upcomingInterviews,
    required this.subscriptionPlan,
    required this.remainingAiCredits,
  });

  factory DashboardSummary.fromJson(Map<String, dynamic> json) {
    return DashboardSummary(
      totalUploadedResumes: json['total_uploaded_resumes'] as int,
      totalGeneratedResumes: json['total_generated_resumes'] as int,
      savedJobs: json['saved_jobs'] as int,
      upcomingInterviews: json['upcoming_interviews'] as int,
      subscriptionPlan: json['subscription_plan'] as String?,
      remainingAiCredits: json['remaining_ai_credits'] as int,
    );
  }
}
