import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Home() {
  return (
    <>
      <div className="min-h-screen">
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-4xl font-bold mb-4">Repo AI</h1>
          <Input
            type="text"
            placeholder="Enter URL"
            className="border border-gray-300 p-2 mb-4 w-1/2"
          />
          <Button className="bg-blue-500 text-white p-2 rounded">
            Process
          </Button>
        </div>
      </div>
    </>
  );
}
