import React from "react";
import  Job_card  from './ui/Job_card2';
import "../index.css";


// Sample job data
const sampleJobs = [
  
  {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },  
  {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },  
  {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
    {
    id: '1',
    title: 'Senior Frontend Developer',
    company: {
      name: 'TechCorp Solutions',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'San Francisco',
      postalCode: '94102',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$120,000 - $160,000/year',
    experience: '5+ years',
    education: "Bachelor's Degree",
    datePosted: '2 days ago',
  },
  {
    id: '2',
    title: 'UX/UI Designer',
    company: {
      name: 'Creative Studio Inc',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'New York',
      postalCode: '10001',
    },
    contractType: 'Contract',
    hours: '30h/week',
    experience: '3+ years',
    education: 'Design Portfolio Required',
    datePosted: '1 week ago',
  },
  {
    id: '3',
    title: 'Junior Software Engineer',
    company: {
      name: 'StartUp Labs',
      logo: 'https://images.unsplash.com/photo-1760386129108-d17b9cdfc4fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWNoJTIwY29tcGFueSUyMGxvZ28lMjBtb2Rlcm58ZW58MXx8fHwxNzcwOTIwMTkzfDA&ixlib=rb-4.1.0&q=80&w=1080',
    },
    location: {
      city: 'Austin',
      postalCode: '78701',
    },
    contractType: 'Full-time',
    hours: '40h/week',
    salary: '$70,000 - $90,000/year',
    experience: '0-2 years',
    education: "Bachelor's in CS",
    datePosted: 'Today',
  },
];

export default function App() {
  const handleApply = (jobId) => {
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xs mx-auto  lg:px-30">
        <h1 className="text-2xl font-bold mb-8 text-gray-900">Available Positions</h1>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          {sampleJobs.map((job) => (
            <Job_card key={job.id} job={job} onApply={handleApply} />
          ))}
        </div>
      </div>
    </div>
  );
}
