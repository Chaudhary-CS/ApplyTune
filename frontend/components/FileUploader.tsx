'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { FileUp, CheckCircle2, AlertCircle, FileText } from 'lucide-react'
import toast from 'react-hot-toast'

interface FileUploaderProps {
  onUpload: (file: File) => void
}

export default function FileUploader({ onUpload }: FileUploaderProps) {
  const [isDragActive, setIsDragActive] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    // Handle rejected files
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0]
      if (rejection.errors[0]?.code === 'file-too-large') {
        toast.error('File too large! Max size is 10MB')
      } else if (rejection.errors[0]?.code === 'file-invalid-type') {
        toast.error('Invalid file type! Please upload PDF or DOCX')
      } else {
        toast.error('File upload failed')
      }
      return
    }

    // Handle accepted files
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0]
      onUpload(file)
    }
  }, [onUpload])

  const { getRootProps, getInputProps, isDragAccept, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
      // Removed .tex - users should paste LaTeX code instead!
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
  })

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          relative border border-dashed rounded-3xl p-16 text-center cursor-pointer
          transition-all duration-300 ease-out
          ${isDragAccept ? 'border-primary-900 bg-gray-50' : ''}
          ${isDragReject ? 'border-red-400 bg-red-50' : ''}
          ${!isDragActive ? 'border-gray-200 hover:border-primary-900 hover:bg-gray-50' : ''}
          bg-white shadow-apple hover:shadow-apple-lg
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-6">
          {/* Icon */}
          <div className={`
            w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-300
            ${isDragAccept ? 'bg-primary-900' : ''}
            ${isDragReject ? 'bg-red-100' : ''}
            ${!isDragActive ? 'bg-gray-100' : ''}
          `}>
            {isDragAccept && <CheckCircle2 className="w-8 h-8 text-white" />}
            {isDragReject && <AlertCircle className="w-8 h-8 text-red-600" />}
            {!isDragActive && <FileUp className="w-8 h-8 text-primary-900" />}
          </div>

          {/* Text */}
          <div>
            <h3 className="text-2xl font-semibold text-primary-900 mb-3 tracking-tight">
              {isDragActive ? 'Drop your resume here' : 'Upload your resume'}
            </h3>
            <p className="text-gray-500 mb-2 font-light">
              Drag and drop, or click to browse
            </p>
            <p className="text-xs text-gray-400 font-light">
              Supports PDF and DOCX · Max 10MB
            </p>
          </div>

          {/* Button */}
          <button
            type="button"
            className="btn-primary mt-2"
          >
            Choose File
          </button>
        </div>

        {/* Tips */}
        <div className="mt-10 pt-8 border-t border-gray-100">
          <p className="text-xs text-gray-400 font-light mb-3 tracking-wide">TIPS FOR BEST RESULTS</p>
          <ul className="text-xs text-gray-500 space-y-2 font-light">
            <li>• Use your most current resume</li>
            <li>• Ensure text is selectable, not in images</li>
            <li>• Simple formatting works best</li>
          </ul>
        </div>
      </div>

      {/* Info cards - Apple style */}
      <div className="grid md:grid-cols-3 gap-3 mt-8">
        {[
          { title: 'Secure', desc: 'Your resume stays private' },
          { title: 'Fast', desc: 'Results in ~30 seconds' },
          { title: 'Free', desc: 'No credit card needed' }
        ].map((item, i) => (
          <div key={i} className="bg-gray-50/50 rounded-2xl p-5 border border-gray-100 text-center">
            <p className="font-medium text-primary-900 text-sm mb-1 tracking-tight">{item.title}</p>
            <p className="text-xs text-gray-500 font-light">{item.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
