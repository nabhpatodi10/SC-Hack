"use client";

import { useState, useRef } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const formSteps = [
  {
    id: 1,
    name: "Personal Information",
    question: "What is your name?",
    placeholder: "Enter your full name",
    options: ["Continue", "Skip"],
    errorBanner: "Personal Information Error",
    errorMessage: "Please fill in all required fields"
  },
  {
    id: 2,
    name: "Record your introduction",
    question: "Please record a video introduction about yourself",
    instructions: "Press 'Start Recording' and speak clearly for up to 30 seconds",
    options: ["Start Recording", "Stop Recording", "Save Recording", "Retry"],
    errorBanner: "Recording Error",
    errorMessage: "Failed to save recording",
  },
  {
    id: 3,
    name: "Select your preferences",
    question: "What is your preferred option?",
    options: ["Option A", "Option B", "Option C"],
    errorBanner: "Selection Error",
    errorMessage: "Please select at least one option"
  }
];

export default function Home() {
  const [step, setStep] = useState(0);
  const [recording, setRecording] = useState(false);
  const [mediaUrl, setMediaUrl] = useState("");
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);

  const currentStep = formSteps[step];

  const formSchema = z.object({ answer: z.string().min(1, "This field is required") });
  const form = useForm({ resolver: zodResolver(formSchema), defaultValues: { answer: "" } });

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      streamRef.current = stream;
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      
      const recorder = new MediaRecorder(stream);
      const chunks = [];
      
      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: "video/webm" });
        setMediaUrl(URL.createObjectURL(blob));
      };
      
      mediaRecorderRef.current = recorder;
      recorder.start();
      setRecording(true);
    } catch (err) {
      console.error("Error accessing media devices:", err);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      streamRef.current.getTracks().forEach(track => track.stop());
      setRecording(false);
    }
  };

  const handleNext = () => {
    if (step < formSteps.length - 1) {
      setStep(step + 1);
      form.reset();
    } else {
      alert("Form completed successfully!");
      setStep(0);
      setMediaUrl("");
      form.reset();
    }
  };

  return (
    <div className="container mx-auto py-10">
      <Card className="max-w-md mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">
            Step {currentStep.id}: {currentStep.name}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg font-medium">{currentStep.question}</p>
          {currentStep.instructions && <p className="text-sm text-gray-500 mt-1">{currentStep.instructions}</p>}
          
          {currentStep.id === 2 && (
            <div className="flex flex-col items-center mt-4">
              <video ref={videoRef} className="w-full aspect-video bg-gray-100 rounded-md mb-4" autoPlay muted />
              {mediaUrl && <video src={mediaUrl} controls className="w-full aspect-video mt-2" />}
            </div>
          )}
          
          {currentStep.id !== 2 && (
            <Form {...form}>
              <form onSubmit={form.handleSubmit(handleNext)} className="space-y-4">
                <FormField
                  control={form.control}
                  name="answer"
                  render={({ field }) => (
                    <FormItem>
                      <FormControl>
                        <Input placeholder={currentStep.placeholder || "Enter your answer"} {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </form>
            </Form>
          )}
        </CardContent>
        <CardFooter className="flex flex-wrap gap-2 justify-center">
          {currentStep.options.map((option, index) => (
            <Button
              key={index}
              onClick={() => {
                if (currentStep.id === 2) {
                  if (option === "Start Recording") startRecording();
                  else if (option === "Stop Recording") stopRecording();
                } else {
                  handleNext();
                }
              }}
              variant="default"
            >
              {option}
            </Button>
          ))}
        </CardFooter>
      </Card>
    </div>
  );
}
