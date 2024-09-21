//using SevenZipExtractor;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace DeadCons_loader
{
    internal class Downloader
    {
        internal static async Task RFD()
        {
            if (!File.Exists("RFD.exe"))
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("RFD.exe not detected");
                Console.ForegroundColor = ConsoleColor.Magenta;
                Console.WriteLine("Starting to download");

                try
                {
                    using (HttpClient client = new HttpClient())
                    {
                        byte[] r = await client.GetByteArrayAsync("https://raw.githubusercontent.com/OwlUniversal/RFD/main/RFD.exe");
                        File.WriteAllBytes("RFD.exe", r);
                    }
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("RFD.exe successfully downloaded");
                }
                catch (Exception)
                {
                    Console.ForegroundColor = ConsoleColor.Red;
                    Console.WriteLine("Cannot download RFD.exe from GitHub, try again later");
                    await Task.Delay(10000);
                    return;
                }
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("RFD.exe detected");
            }

        }
/*
        internal static async Task Roblox()
        {
            if (!Directory.Exists("Roblox"))
            {
                string url = "https://github.com/Windows81/Roblox-Filtering-Disabled/releases/download/2024-06-12T0810Z/v463.Player.7z";
                string currentDirectory = Directory.GetCurrentDirectory();
                string downloadPath = Path.Combine(Path.GetTempPath(), "v463.Player.7z");


                string extractPath = Path.Combine(currentDirectory, "Roblox");
                // Загрузка файла
                using (HttpClient client = new HttpClient())
                {
                    Console.WriteLine("Downloading Roblox Player v463...");
                    byte[] data = await client.GetByteArrayAsync(url);
                    File.WriteAllBytes(downloadPath, data);
                    Console.WriteLine("Download complete.");
                }

                Console.WriteLine("Unpacking file...");
                Directory.CreateDirectory(extractPath);

                using (ArchiveFile archiveFile = new ArchiveFile(downloadPath))
                {
                    int count = archiveFile.Entries.Count;
                    int i = 0;
                    Parallel.ForEach(archiveFile.Entries, entry =>
                    {
                        int index = System.Threading.Interlocked.Increment(ref i); // Обеспечение корректного счёта

                        Console.Write($"\r[{index}/{count}]"); // Обновление прогресса

                        if (!entry.IsFolder)
                        {
                            string destinationPath = Path.Combine(extractPath, entry.FileName);

                            // Создание каталога, если его нет
                            Directory.CreateDirectory(Path.GetDirectoryName(destinationPath));

                            // Распаковка файла
                            entry.Extract(destinationPath);
                        }
                    });
                }
                Console.WriteLine($"Unpacking complete. Files extracted to: {extractPath}");

                // Удаление временного файла
                File.Delete(downloadPath);
            }
            else
            {
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("Roblox folder detected");
            }

        }
   */
    }
}
