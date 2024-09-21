using DeadCons_loader;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace DeadCons_loader_4._8
{
    internal class Program
    {
        static async Task Main(string[] args)
        {
            Console.Title = "DeadCons joiner";
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Red;

            await Downloader.RFD();
            //await Downloader.Roblox();

            Console.ForegroundColor = ConsoleColor.White;

            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "RFD.exe",
                Arguments = @"player -rh ""46.8.232.164"" -rp 2005 -wp 2008 -u ""923423443""",
                UseShellExecute = true,
                RedirectStandardOutput = false, 
                RedirectStandardError = false,  
                CreateNoWindow = false 
            };

            try
            {
                using (Process process = Process.Start(startInfo))
                {
                    if (process == null)
                    {
                        Console.WriteLine("Failed to start process.");
                    }
                    else
                    {
                        Console.WriteLine("Process started successfully.");
                        process.WaitForExit();
                        Console.WriteLine("Process exited.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("An error occurred while starting the process:");
                Console.WriteLine(ex.Message);
            }
            Console.WriteLine("Process exited.");


            await Task.Delay(10000);

        }
    }
}
