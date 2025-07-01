# GitHub Release Guide

## Overview
This guide explains how to deploy your Star Wars: Rebellion Community Fix Installer to GitHub Releases. The project is fully configured with automated workflows and multiple build options for reliable deployment.

## Project Status
✅ **Build System Ready** - Multiple tested build scripts  
✅ **GitHub Actions Configured** - Automated release workflow  
✅ **Windows Executable Built** - 56MB standalone installer with custom icon  
✅ **Documentation Complete** - Comprehensive user and developer guides  

You have three deployment options: **Automatic Release**, **Manual Release**, or **Quick Release**.

## Option 1: Automatic Release (Recommended)

### How It Works
The GitHub Actions workflow automatically:
- Builds the Windows executable on GitHub's servers
- Creates the distribution package
- Generates a release with proper description and files
- Handles all dependencies and build complexities

### Step 1: Push Your Code
```bash
git add .
git commit -m "Release v2.63.1.0 - Star Wars Rebellion Community Fix"
git push origin main
```

### Step 2: Create and Push Tag
```bash
git tag v2.63.1.0
git push origin v2.63.1.0
```

The GitHub Actions workflow will automatically:
1. Build the executable with your custom rebexe2.ico icon
2. Create the distribution package
3. Generate a professional release with description
4. Upload the ZIP file for users to download

## Option 2: Manual Release (For local control)

### Step 1: Choose Your Build Method

**Method A: Full Release Preparation**
```bash
python prepare_release.py
```

**Method B: Quick Release (if executable exists)**
```bash
python quick_release.py
```

**Method C: Fix PyInstaller Issues**
```bash
python fix_pyinstaller.py
```

**Method D: Windows Batch Script**
```bash
build.bat
```

These scripts will:
- Handle PyInstaller dependencies and conflicts
- Build the standalone Windows executable (56MB)
- Include the custom rebexe2.ico icon
- Create the distribution package
- Generate a ZIP file ready for upload

### Step 2: Set Up GitHub Repository
1. **Create a new repository** on GitHub (if you haven't already)
2. **Push your code** to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Star Wars Rebellion Community Fix Installer"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

### Step 3: Create the GitHub Release
1. Go to your GitHub repository
2. Click **"Releases"** (on the right side of the repository page)
3. Click **"Create a new release"**
4. Fill in the release details:
   - **Tag version**: `v2.63.1.0`
   - **Release title**: `Star Wars: Rebellion Community Fix v2.63.1.0`
   - **Description**: Copy the description from the workflow file
5. **Upload the ZIP file** created by the preparation script
6. Click **"Publish release"**

## Option 3: Quick Release (If executable already built)

If you've already built the executable locally and just need to package it:

```bash
python quick_release.py
```

This lightweight script:
- Uses your existing built executable
- Creates the distribution package
- Generates the ZIP file for manual upload
- Perfect for rapid iterations

## Release Package Contents

Your release will include:
```
Star_Wars_Rebellion_Community_Fix_v2.63.1.0.zip
├── Star_Wars_Rebellion_Community_Fix_Installer.exe
├── D3Dlmm.dll
├── d3drm.dll  
├── DDraw.dll
├── REBEXE.exe
├── README.md
├── LICENSE
└── INSTALLATION_INSTRUCTIONS.txt
```

## User Instructions (for your release description)

```markdown
## Star Wars: Rebellion Community Fix v2.63.1.0

### Features
- ✅ Automatic game detection (GOG, Steam, Original versions)  
- ✅ Safe backup creation with timestamps
- ✅ Critical shortcut modification with -w flag
- ✅ Windows XP compatibility configuration
- ✅ Steam version detection and warnings
- ✅ Complete uninstall/restore functionality

### Installation
1. Download the ZIP file below
2. Extract all files to a folder
3. Run `Star_Wars_Rebellion_Community_Fix_Installer.exe`
4. Follow the installer instructions

### System Requirements
- Windows 7/8/10/11 (32-bit or 64-bit)
- Star Wars: Rebellion (any version)
- 50MB free disk space  
- Administrator privileges (for Program Files installations)

### Files Included
- Main installer executable
- All required patch files (D3Dlmm.dll, d3drm.dll, DDraw.dll, REBEXE.exe)
- Documentation and instructions
```

## Testing Your Release

After creating the release:
1. **Download the ZIP file** from your GitHub release
2. **Extract it on a clean Windows machine**
3. **Run the installer** to verify it works correctly
4. **Test all features**: auto-detection, manual selection, installation, uninstall

## Build Script Comparison

| Script | Use Case | Requirements | Output |
|--------|----------|--------------|---------|
| `prepare_release.py` | Complete release preparation | Python, PyInstaller | Full build + ZIP |
| `quick_release.py` | Package existing build | Python, existing exe | ZIP from existing files |
| `fix_pyinstaller.py` | Handle PyInstaller conflicts | Python | Fixed build + ZIP |
| `build.bat` | Windows native build | Windows, Python | Windows-optimized build |
| GitHub Actions | Automated cloud build | Git repository | Automatic release |

## Troubleshooting

### Build Issues:
- **"Missing patch files"**: Ensure D3Dlmm.dll, d3drm.dll, DDraw.dll, REBEXE.exe are in project root
- **"PyInstaller pathlib conflict"**: Run `python fix_pyinstaller.py` to resolve
- **"Permission denied"**: Windows file locks - scripts now handle this automatically
- **"Icon not found"**: icon.ico is created from rebexe2.ico in attached_assets

### GitHub Actions Issues:
- **Workflow not running**: Ensure `.github/workflows/release.yml` is pushed to repository
- **Build fails**: Check Actions tab for detailed logs
- **Release not created**: Verify tag was pushed correctly (`git push origin v2.63.1.0`)

### Windows-Specific Issues:
- **UAC prompts**: Normal for PyInstaller builds, users can safely allow
- **Antivirus warnings**: Common with PyInstaller executables, add to exceptions
- **File permissions**: All build scripts now handle Windows readonly attributes

## Next Steps

Once your release is published:
1. **Share the GitHub release link** with users
2. **Monitor the Issues tab** for user feedback
3. **Update the version** in your code for future releases
4. **Create new releases** by pushing new tags (e.g., `v2.63.1.1`)

## Security Note

Windows Defender may flag the executable initially (common with PyInstaller). Users can safely add it to their antivirus exceptions. For production releases, consider code signing certificates to avoid security warnings.