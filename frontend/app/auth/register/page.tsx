import { RegisterForm } from '@/components/auth/RegisterForm'

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-[#0A2342] mb-2">Blackletter Systems</h1>
          <p className="text-gray-600">Old rules. New game.</p>
        </div>
        <RegisterForm />
      </div>
    </div>
  )
}
