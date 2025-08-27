import { SignUp } from '@clerk/nextjs'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

export default function Page() {
  return (
    <div className="min-h-screen bg-page">
      <div className="absolute top-4 left-4">
        <Link
          href="/"
          className="p-2 hover-surface rounded-full transition-colors inline-flex items-center"
        >
          <ArrowLeft className="w-5 h-5" />
        </Link>
      </div>
      <div className="flex items-center justify-center min-h-screen">
        <SignUp 
          path="/sign-up"
          routing="path"
          signInUrl="/sign-in"
          redirectUrl="/"
        />
      </div>
    </div>
  )
}
