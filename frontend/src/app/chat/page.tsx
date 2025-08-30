"use client";
import {useState} from "react";
import {useRouter} from "next/navigation";
import { BookOpen, Sparkles, Cpu, MessageSquare, Mic, Image, ArrowLeft } from "lucide-react";

type Subject = {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  units: string[];
};

const subjects: Subject[] = [
  {
    id: "Generative AI",
    name: "Generative AI",
    description: "Chatbots, Image Generation, Code Generation, Creative AI",
    icon: <Sparkles className="w-8 h-8" />,
    color: "blue",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Edge AI",
    name: "Edge AI",
    description: "Edge Computing, IoT AI, Real-time Processing",
    icon: <Cpu className="w-8 h-8" />,
    color: "green",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Statistical Natural Language Processing",
    name: "Statistical Natural Language Processing",
    description: "Text Analysis, Language Models, Sentiment Analysis",
    icon: <MessageSquare className="w-8 h-8" />,
    color: "purple",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Speech Processing",
    name: "Speech Processing",
    description: "Speech Recognition, Audio Analysis, Voice Synthesis",
    icon: <Mic className="w-8 h-8" />,
    color: "orange",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  },
  {
    id: "Image Processing and Vision Techniques",
    name: "Image Processing and Vision Techniques",
    description: "Computer Vision, Image Analysis, Pattern Recognition",
    icon: <Image className="w-8 h-8" />,
    color: "indigo",
    units: ["Unit 1", "Unit 2", "Unit 3", "Unit 4", "Unit 5"]
  }
];

export default function HomePage() {
  const router = useRouter();

  const handleSubjectClick = (subject: Subject) => {
    // Navigate to advanced chat with subject context
    router.push(`/chat/advanced?subject=${subject.id}&name=${encodeURIComponent(subject.name)}`);
  };

  return (
    <div className="min-h-screen bg-page">
      {/* Header Section */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex items-center mb-8">
          <button
            onClick={() => router.push('/')}
            className="p-2 hover-surface rounded-full transition-colors mr-4"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="text-center flex-1">
            <h1 className="text-3xl font-bold text-primary mb-2">
              College Study Assistant
            </h1>
            <p className="text-secondary text-lg">
              Get AI-powered help with your subjects. Select a subject to start learning!
            </p>
          </div>
        </div>

        {/* Subjects Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
          {subjects.map((subject) => (
            <div
              key={subject.id}
              onClick={() => handleSubjectClick(subject)}
              className="cursor-pointer rounded-xl border border-default bg-surface p-6 transition-all duration-200 hover:shadow-lg hover:border-strong"
            >
              <div className="flex flex-col items-center text-center space-y-4">
                <div className="p-3 rounded-full bg-surface-muted text-secondary">
                  {subject.icon}
                </div>
                <div>
                  <h3 className="font-semibold text-lg text-primary mb-2">
                    {subject.name}
                  </h3>
                  <p className="text-sm text-secondary">
                    {subject.description}
                  </p>
                </div>
                <div className="text-xs text-low">
                  {subject.units.length} Units Available
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
