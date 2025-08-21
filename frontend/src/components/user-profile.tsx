'use client'

import { useUser, useAuth } from '@clerk/nextjs'

export function UserProfile() {
  const { user, isLoaded } = useUser()
  const { signOut } = useAuth()

  if (!isLoaded) {
    return <div>Loading...</div>
  }

  if (!user) {
    return <div>No user found</div>
  }

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">User Profile</h2>
      
      {/* User's profile picture */}
      {user.imageUrl && (
        <img 
          src={user.imageUrl} 
          alt="Profile" 
          className="w-20 h-20 rounded-full mb-4"
        />
      )}
      
      {/* User information from Clerk */}
      <div className="space-y-2">
        <p><strong>Name:</strong> {user.fullName || 'No name provided'}</p>
        <p><strong>Email:</strong> {user.primaryEmailAddress?.emailAddress}</p>
        <p><strong>User ID:</strong> {user.id}</p>
        <p><strong>Created:</strong> {user.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'Unknown'}</p>
        
        {/* OAuth provider info */}
        <div>
          <strong>Connected accounts:</strong>
          <ul className="mt-1">
            {user.externalAccounts.map((account) => (
              <li key={account.id} className="text-sm text-gray-600">
                {account.provider} - {account.emailAddress}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <button 
        onClick={() => signOut()}
        className="mt-4 w-full px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
      >
        Sign Out
      </button>
    </div>
  )
}
