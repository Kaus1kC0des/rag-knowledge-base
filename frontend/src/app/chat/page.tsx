"use client";
import {useState} from "react";
import {useRouter} from "next/navigation";
import { BookOpen, Calculator, Atom, Cpu, Lightbulb, ArrowLeft } from "lucide-react";

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
    id: "mathematics",
    name: "Mathematics",
    description: "Calculus, Linear Algebra, Statistics",
    icon: <Calculator className="w-8 h-8" />,
    color: "blue",
    units: ["Unit 1: Differential Calculus", "Unit 2: Integral Calculus", "Unit 3: Linear Algebra", "Unit 4: Probability", "Unit 5: Statistics"]
  },
  {
    id: "physics",
    name: "Physics",
    description: "Mechanics, Thermodynamics, Electromagnetism",
    icon: <Atom className="w-8 h-8" />,
    color: "purple",
    units: ["Unit 1: Classical Mechanics", "Unit 2: Thermodynamics", "Unit 3: Electromagnetism", "Unit 4: Optics", "Unit 5: Modern Physics"]
  },
  {
    id: "computer-science",
    name: "Computer Science",
    description: "Algorithms, Data Structures, Programming",
    icon: <Cpu className="w-8 h-8" />,
    color: "green",
    units: ["Unit 1: Programming Fundamentals", "Unit 2: Data Structures", "Unit 3: Algorithms", "Unit 4: Database Systems", "Unit 5: Software Engineering"]
  },
  {
    id: "engineering",
    name: "Engineering",
    description: "Circuit Analysis, Control Systems, Signals",
    icon: <Lightbulb className="w-8 h-8" />,
    color: "orange",
    units: ["Unit 1: Circuit Analysis", "Unit 2: Control Systems", "Unit 3: Signal Processing", "Unit 4: Power Systems", "Unit 5: Communication Systems"]
  },
  {
    id: "general-studies",
    name: "General Studies",
    description: "Literature, History, Philosophy",
    icon: <BookOpen className="w-8 h-8" />,
    color: "indigo",
    units: ["Unit 1: Literature", "Unit 2: History", "Unit 3: Philosophy", "Unit 4: Economics", "Unit 5: Political Science"]
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
