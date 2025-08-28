import { auth, currentUser } from '@clerk/nextjs/server'
import { UserProfile } from '@/components/user-profile'
import { redirect } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

export default async function ProfilePage() {
  // Get user authentication status
  const { userId } = await auth()
  
  // If not authenticated, redirect to sign-in
  if (!userId) {
    redirect('/sign-in')
  }

  // Get current user data from Clerk (server-side)
  const user = await currentUser()

  return (
    <div className="min-h-screen bg-page py-12">
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex items-center mb-8">
          <Link
            href="/"
            className="p-2 hover-surface rounded-full transition-colors mr-4"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <h1 className="text-3xl font-bold flex-1 text-center">User Profile</h1>
        </div>
        
        {/* Client-side user profile component */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Client-Side User Data (from useUser hook):</h2>
          <UserProfile />
        </div>

        {/* Server-side user data */}
        <div className="bg-surface rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Server-Side User Data (from currentUser()):</h2>
          
          {user && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <strong>User ID:</strong> 
                  <p className="text-sm text-secondary break-all">{user.id}</p>
                </div>
                <div>
                  <strong>Email:</strong> 
                  <p className="text-sm text-secondary">{user.primaryEmailAddress?.emailAddress}</p>
                </div>
                <div>
                  <strong>Full Name:</strong> 
                  <p className="text-sm text-secondary">{user.fullName || 'Not provided'}</p>
                </div>
                <div>
                  <strong>Username:</strong> 
                  <p className="text-sm text-secondary">{user.username || 'Not set'}</p>
                </div>
              </div>

              <div>
                <strong>Email Addresses:</strong>
                <ul className="mt-2 space-y-1">
                  {user.emailAddresses.map((email) => (
                    <li key={email.id} className="text-sm text-secondary">
                      {email.emailAddress} {email.id === user.primaryEmailAddressId && '(Primary)'}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <strong>External Accounts (OAuth):</strong>
                <ul className="mt-2 space-y-1">
                  {user.externalAccounts.map((account) => (
                    <li key={account.id} className="text-sm text-secondary">
                      <span className="font-medium">{account.provider}</span> - {account.emailAddress}
                      <br />
                      <span className="text-xs text-low">
                        Provider ID: {account.externalId} | Username: {account.username || 'N/A'}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <strong>Account Created:</strong>
                <p className="text-sm text-secondary">
                  {user.createdAt ? new Date(user.createdAt).toLocaleString() : 'Unknown'}
                </p>
              </div>

              <div>
                <strong>Last Updated:</strong>
                <p className="text-sm text-secondary">
                  {user.updatedAt ? new Date(user.updatedAt).toLocaleString() : 'Unknown'}
                </p>
              </div>

              <div>
                <strong>Profile Image:</strong>
                {user.imageUrl ? (
                  <div className="mt-2">
                    <img 
                      src={user.imageUrl} 
                      alt="Profile" 
                      className="w-16 h-16 rounded-full"
                    />
                    <p className="text-xs text-low mt-1">{user.imageUrl}</p>
                  </div>
                ) : (
                  <p className="text-sm text-secondary">No image</p>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="mt-8 text-center">
          <a 
            href="/"
            className="btn-primary text-inverse px-6 py-2 rounded-lg transition"
          >
            Back to Home
          </a>
        </div>
      </div>
    </div>
  )
}
