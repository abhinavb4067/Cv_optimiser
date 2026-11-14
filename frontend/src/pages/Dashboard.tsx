import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { api } from "../lib/api";

const NAV_ITEMS = [
  "Dashboard",
  "My Resumes",
  "AI Resume Builder",
  "ATS Resume Scanner",
  "Job Recommendations",
  "Skill Gap Analysis",
  "Career Roadmap",
  "AI Mock Interviews",
  "Cover Letter Generator",
  "LinkedIn Optimizer",
  "Portfolio Builder",
  "Job Application Tracker",
  "Career & Salary Insights",
  "Subscription & Billing",
  "Settings",
];

interface Summary {
  total_uploaded_resumes: number;
  total_generated_resumes: number;
  saved_jobs: number;
  upcoming_interviews: number;
  subscription_plan: string | null;
  remaining_ai_credits: number;
}

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    api.get<Summary>("/dashboard/summary").then(({ data }) => setSummary(data));
  }, []);

  return (
    <div className="flex min-h-screen bg-gray-50">
      <aside className="w-64 shrink-0 border-r border-gray-200 bg-white p-4">
        <h2 className="mb-4 px-2 text-lg font-semibold text-gray-900">Career Assistant</h2>
        <nav className="space-y-1">
          {NAV_ITEMS.map((item, i) => (
            <div
              key={item}
              className={`cursor-pointer rounded-md px-3 py-2 text-sm ${
                i === 0 ? "bg-indigo-50 font-medium text-indigo-700" : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              {item}
            </div>
          ))}
        </nav>
      </aside>

      <main className="flex-1 p-8">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-gray-900">Welcome, {user?.full_name ?? user?.email}</h1>
            <p className="text-sm text-gray-500">Role: {user?.role}</p>
          </div>
          <button
            onClick={logout}
            className="rounded-md border border-gray-300 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            Log out
          </button>
        </div>

        {summary && (
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <StatCard label="Uploaded Resumes" value={summary.total_uploaded_resumes} />
            <StatCard label="Generated Resumes" value={summary.total_generated_resumes} />
            <StatCard label="Saved Jobs" value={summary.saved_jobs} />
            <StatCard label="Upcoming Interviews" value={summary.upcoming_interviews} />
            <StatCard label="AI Credits Remaining" value={summary.remaining_ai_credits} />
            <StatCard label="Subscription Plan" value={summary.subscription_plan ?? "Free"} />
          </div>
        )}
      </main>
    </div>
  );
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
      <p className="text-xs uppercase tracking-wide text-gray-500">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-gray-900">{value}</p>
    </div>
  );
}
