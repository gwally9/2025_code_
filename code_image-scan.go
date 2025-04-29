package main

import (
        "image"
        _ "image/png"
        "io/ioutil"
        "log"
        "os"
)

func main() {
        rootDir := "./images/" // adjust this to the directory containing your PNG files

        err := generateThumbnails(rootDir)
        if err != nil {
                log.Fatal(err)
        }
}

func generateThumbnails(dir string) error {
        files, err := ioutil.ReadDir(dir)
        if err != nil {
                return err
        }

        for _, file := range files {
                if !file.IsDir() && file.Extension() == ".png" {
                        pngFile := dir + file.Name()
                        thumbnailFile := dir + "thumb-" + file.Name()

                        // Read the PNG image
                        fileBytes, err := ioutil.ReadFile(pngFile)
                        if err != nil {
                                return err
                        }

                        img, _, err := image.Decode(bytes.NewReader(fileBytes))
                        if err != nil {
                                return err
                        }

                        // Create a thumbnail of the image (resize to 100x100 pixels)
                        maxWidth := 100
                        maxHeight := 100
                        ratio := float64(maxWidth) / float64(img.Bounds().Dx())
                        newHeight := int(float64(img.Bounds().Dy()) * ratio)
                        if newHeight > maxHeight {
                                newHeight = maxHeight
                                ratio = float64(maxHeight) / float64(img.Bounds().Dy())
                                newWidth := int(float64(img.Bounds().Dx()) * ratio)
                                if newWidth > maxWidth {
                                        newWidth = maxWidth
                                }
                        } else {
                                newWidth = int(float64(img.Bounds().Dx()) * ratio)
                        }

                        thumb := image.NewRGBA(image.Rect(0, 0, newWidth, newHeight))
                        draw.Draw(thumb, thumb.Bounds(), img, (img.Bounds().Min.X+int((img.Bounds().Dx()-newWidth)/2)), (img.Bounds().Min.Y+int((img.Bounds().Dy()-newHeight)/2)), image.OpCopy)

                        // Save the thumbnail
                        err = ioutil.WriteFile(thumbnailFile, thumb.Pix[:], 0644)
                        if err != nil {
                                return err
                        }
                }
        }

        return nil
}

func (f *os.FileInfo) Extension() string {
        return filepath.Ext(f.Name())
}
```
Here's how the code works:

1. The `main` function sets the root directory containing the PNG files and calls the `generateThumbnails` function.
2. The `generateThumbnails` function reads all files in the specified directory using `ioutil.ReadDir`. It then iterates over the files, checking if each file is a PNG image (using the `.Extension()` method to check the file extension).
3. For each PNG file, it reads the file contents using `ioutil.ReadFile`, decodes the PNG image using the `image` package, and creates a thumbnail of the image by resizing it to 100x100 pixels.
4. The thumbnail is then saved as a new file with the same name as the original file, but prefixed with "thumb-".

Note that this code assumes that all PNG files are located in the specified directory and its subdirectories. You may need to modify the code to scan other directories or handle different types of images.

Also, this code uses the `image` package to decode and manipulate the image data. This package is part of the Go standard library, so you don't need to install any additional dependencies. However, if you want to use other image formats (e.g., JPEG), you may need to install additional packages or libraries.
