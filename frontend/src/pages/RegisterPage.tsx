import { useState } from "react";
import type { FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Check, X } from "lucide-react";
import toast from "react-hot-toast";
import clsx from "clsx";
import { AuthLayout } from "@/components/auth/AuthLayout";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { ApiError } from "@/api/client";

const RULES: { label: string; test: (pw: string) => boolean }[] = [
  { label: "At least 8 characters", test: (pw) => pw.length >= 8 },
  { label: "One uppercase letter", test: (pw) => /[A-Z]/.test(pw) },
  { label: "One lowercase letter", test: (pw) => /[a-z]/.test(pw) },
  { label: "One number", test: (pw) => /\d/.test(pw) },
  {
    label: "One special character",
    test: (pw) => /[!@#$%^&*()_\-+=[\]{}|\\:;"'<>,.?/~`]/.test(pw),
  },
];

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  // Note: internally still called "username" because that's what the
  // backend column/field is named — only the on-screen label changes.
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<string[]>([]);

  const allRulesPass = RULES.every((rule) => rule.test(password));
  const passwordsMatch = confirmPassword.length === 0 || confirmPassword === password;
  const showMismatch = confirmPassword.length > 0 && confirmPassword !== password;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErrors([]);

    if (password !== confirmPassword) {
      setErrors(["Passwords do not match."]);
      return;
    }

    setIsSubmitting(true);

    try {
      await register({ username, email, password });
      navigate("/chat", { replace: true });
    } catch (err) {
      if (err instanceof ApiError) {
        setErrors(err.errors && err.errors.length > 0 ? err.errors : [err.message]);
        toast.error(err.message);
      } else {
        toast.error("Unable to create account.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthLayout title="Create your account" subtitle="Start troubleshooting with ProdPilot AI.">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Input
          label="Full Name"
          autoComplete="name"
          required
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Jane Doe"
        />
        <Input
          label="Email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@company.com"
        />
        <Input
          label="Password"
          type="password"
          autoComplete="new-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
        />
        <Input
          label="Confirm Password"
          type="password"
          autoComplete="new-password"
          required
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="••••••••"
          error={showMismatch ? "Passwords don't match." : undefined}
        />

        {password.length > 0 && (
          <ul className="grid grid-cols-1 gap-1 rounded-lg bg-slate-50 p-2.5 sm:grid-cols-2">
            {RULES.map((rule) => {
              const passed = rule.test(password);
              return (
                <li
                  key={rule.label}
                  className={clsx(
                    "flex items-center gap-1.5 text-xs",
                    passed ? "text-emerald-600" : "text-slate-400",
                  )}
                >
                  {passed ? <Check className="h-3 w-3" /> : <X className="h-3 w-3" />}
                  {rule.label}
                </li>
              );
            })}
          </ul>
        )}

        {errors.length > 0 && (
          <ul className="list-inside list-disc text-sm text-red-600">
            {errors.map((message) => (
              <li key={message}>{message}</li>
            ))}
          </ul>
        )}

        <Button
          type="submit"
          className="mt-2 w-full"
          isLoading={isSubmitting}
          disabled={!allRulesPass || !username || !email || !passwordsMatch || !confirmPassword}
        >
          Create account
        </Button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-500">
        Already have an account?{" "}
        <Link to="/login" className="font-medium text-brand-600 hover:underline">
          Log in
        </Link>
      </p>
    </AuthLayout>
  );
}