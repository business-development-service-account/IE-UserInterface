'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const Navigation: React.FC = () => {
  const pathname = usePathname()

  const navItems = [
    {
      name: 'Projects',
      href: '/projects',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        </svg>
      )
    },
    {
      name: 'Collections',
      href: '/collections',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
        </svg>
      )
    },
    {
      name: 'Settings',
      href: '/settings',
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="3"></circle>
          <path d="M12 1v6m0 6v6m5.2-15.2l-4.2 4.2m-4.2 4.2l-4.2 4.2m15.2-5.2h-6m-6 0H1m20.2 5.2l-4.2-4.2m-4.2-4.2l-4.2-4.2"></path>
        </svg>
      )
    }
  ]

  return (
    <nav className="w-[60px] bg-sidebar-dark flex flex-col items-center py-5">
      {navItems.map((item) => (
        <Link
          key={item.name}
          href={item.href}
          className={`
            w-[40px] h-[40px] my-2.5 rounded-lg flex items-center justify-center
            transition-all duration-300 cursor-pointer
            ${pathname === item.href
              ? 'bg-accent-blue text-white'
              : 'text-text-light hover:bg-sidebar-hover hover:text-gray-100'
            }
          `}
          title={item.name}
        >
          {item.icon}
        </Link>
      ))}
    </nav>
  )
}

export default Navigation