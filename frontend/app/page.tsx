'use client'
import { useEffect, useRef, useState } from 'react'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Gradient } from '@/components/gradient'

export default function Component() {
  const [repoUrl, setRepoUrl] = useState('')
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    const gradient = new Gradient()
    // @ts-ignore
    gradient.initGradient('#gradient-canvas')
  }, [])

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const repoPath = repoUrl.match(/github\.com\/([^\/]+\/[^\/]+)/)?.[1]

    console.log('Repo path:', repoPath)

    try {
      const response = await fetch('https://d3n.fly.dev/repository/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repository: repoPath }),
      })

      const data = await response.json()
      console.log('Response from API:', data)
    } catch (error) {
      console.error('Error posting data:', error)
    }
  }

  return (
    <main className='flex min-h-screen flex-col items-center justify-center p-4 text-gray-50'>
      <div style={{ position: 'absolute', top: 0, left: 0, bottom: 0, right: 0, zIndex: -2 }}>
        <canvas ref={canvasRef} id='gradient-canvas' />
      </div>
      <div className='container text-center mxx-auto max-w-md space-y-6'>
        <p>
          <code>https://d3n.run</code>
        </p>
        <h1 className='text-8xl'>d3n</h1>
        <p>the k8s of agent orchestration</p>
        {!success ? (
          <form className='space-y-4' onSubmit={handleSubmit}>
            <div className='space-y-2'>
              <Label className='text-sm font-normal' htmlFor='repo-url'>
                Enter a github url and we&apos;ll have one Devin orchestrate a fleet of devins to work on the issues in that Repo
              </Label>
              <Input
                className='w-full rounded-md border-gray-200 bg-white p-2 text-white focus:border-gray-400 focus:outline-none'
                id='repo-url'
                placeholder='https://github.com/user/repo'
                type='text'
                value={repoUrl}
                onChange={e => setRepoUrl(e.target.value)}
              />
            </div>
            <Button
              className='w-full rounded-md bg-white py-2 font-medium text-gray-900 transition-colors hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-400 disabled:cursor-not-allowed disabled:opacity-50'
              type='submit'
            >
              Submit
            </Button>
          </form>
        ) : (
          <p>Open Devin to watch the magic.</p>
        )}
      </div>
    </main>
  )
}
