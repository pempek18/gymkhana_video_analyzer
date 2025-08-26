# Release Guide - Gymkhana Video Analyzer

This guide explains how to automatically build and release executable (.exe) files for the Gymkhana Video Analyzer using GitHub Actions.

## 🚀 Automated Build & Release System

The project includes a complete automated build system that:
- Builds Windows executables automatically
- Creates GitHub releases with downloadable files
- Packages everything into convenient ZIP files
- Triggers on version tags or manual workflow runs

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **GitHub Actions**: Enabled by default on public repositories
3. **Git Tags**: Used to trigger releases

## 🔧 Setup Instructions

### 1. Push Your Code to GitHub

```bash
git add .
git commit -m "Initial commit: Gymkhana Video Analyzer"
git push origin main
```

### 2. Create Your First Release

#### Option A: Using Git Tags (Recommended)

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

#### Option B: Using GitHub Web Interface

1. Go to your repository on GitHub
2. Click "Releases" on the right side
3. Click "Create a new release"
4. Choose a tag (e.g., `v1.0.0`)
5. Write release notes
6. Click "Publish release"

### 3. Monitor the Build Process

1. Go to your repository
2. Click "Actions" tab
3. Watch the "Build and Release Executable" workflow
4. Wait for completion (usually 5-10 minutes)

## 📦 What Gets Built

The automated system creates:

- **`GymkhanaVideoAnalyzer.exe`** - Standalone executable
- **`GymkhanaVideoAnalyzer-Windows.zip`** - Complete package with:
  - Executable file
  - README.md
  - Requirements.txt
  - Launch.bat (easy startup script)

## 🎯 Release Workflow

### Automatic Release (Recommended)

1. **Make Changes**: Update your code
2. **Commit & Push**: Save changes to GitHub
3. **Create Tag**: `git tag v1.1.0 && git push origin v1.1.0`
4. **Auto-Build**: GitHub Actions automatically builds and releases
5. **Download**: Users can download from GitHub Releases

### Manual Release

1. Go to Actions tab in your repository
2. Click "Build and Release Executable"
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## 🔄 Version Management

### Semantic Versioning

Use semantic versioning for your tags:

- **v1.0.0** - Major release (new features)
- **v1.1.0** - Minor release (improvements)
- **v1.1.1** - Patch release (bug fixes)

### Example Release Cycle

```bash
# Initial release
git tag v1.0.0
git push origin v1.0.0

# Add new feature
git add .
git commit -m "Add video export feature"
git push origin main

# Release new version
git tag v1.1.0
git push origin v1.1.0

# Bug fix
git add .
git commit -m "Fix timeline synchronization issue"
git push origin main

# Patch release
git tag v1.1.1
git push origin v1.1.1
```

## 📱 User Experience

### For End Users

1. **Download**: Go to GitHub Releases
2. **Extract**: Download and extract ZIP file
3. **Run**: Double-click `GymkhanaVideoAnalyzer.exe` or `Launch.bat`
4. **No Installation**: Works immediately without Python setup

### Benefits

- ✅ **No Python Required**: Users don't need Python installed
- ✅ **No Dependencies**: All libraries bundled in executable
- ✅ **Easy Distribution**: Single file or ZIP package
- ✅ **Professional**: Looks like commercial software
- ✅ **Cross-Platform Ready**: Can be extended for other OS

## 🛠️ Customization

### Adding an Icon

1. Create an `icon.ico` file in your project root
2. The build system will automatically include it
3. Icon will appear in Windows Explorer and taskbar

### Modifying Build Settings

Edit `GymkhanaVideoAnalyzer.spec` to:
- Change executable name
- Add more hidden imports
- Modify packaging options
- Include additional data files

### Build Script Customization

Edit `build_exe.py` to:
- Change PyInstaller options
- Modify package structure
- Add post-build steps
- Customize installer creation

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails**: Check GitHub Actions logs for error details
2. **Missing Dependencies**: Ensure all imports are in `hiddenimports`
3. **Large Executable**: Use `--onefile` for single file, `--onedir` for folder
4. **Antivirus False Positive**: Common with PyInstaller, submit to antivirus vendors

### Debug Build

For debugging, modify the spec file:

```python
console=True,  # Show console window
debug=True,    # Include debug information
```

### Local Testing

Test the build process locally:

```bash
# Install PyInstaller
pip install pyinstaller

# Run build script
python build_exe.py

# Test executable
./dist/GymkhanaVideoAnalyzer.exe
```

## 📈 Advanced Features

### Multiple Platforms

Extend the workflow for multiple platforms:

```yaml
# In .github/workflows/build-release.yml
jobs:
  build-windows:
    runs-on: windows-latest
    # Windows build steps
    
  build-linux:
    runs-on: ubuntu-latest
    # Linux build steps
    
  build-macos:
    runs-on: macos-latest
    # macOS build steps
```

### Code Signing

For professional distribution, add code signing:

```yaml
- name: Sign Executable
  run: |
    # Code signing commands
    # Requires certificates and signing tools
```

### Automated Testing

Add tests before building:

```yaml
- name: Run Tests
  run: |
    python -m pytest tests/
    
- name: Build executable
  run: |
    python build_exe.py
```

## 🎉 Success Metrics

### What Success Looks Like

- ✅ Automated builds complete successfully
- ✅ Executables run without errors
- ✅ Users can download from GitHub Releases
- ✅ No Python installation required for end users
- ✅ Professional software appearance

### Monitoring

- Watch GitHub Actions for build success rates
- Monitor release downloads
- Check user feedback and issues
- Track version adoption

## 🔮 Future Enhancements

### Potential Improvements

1. **Auto-updater**: Built-in update checking
2. **Installer**: Professional Windows installer (NSIS/Inno Setup)
3. **Portable Mode**: Settings stored with executable
4. **Multi-language**: Internationalization support
5. **Plugin System**: Extensible architecture

### Community Contributions

- Encourage users to report issues
- Accept pull requests for improvements
- Maintain compatibility with different Python versions
- Document API for extensions

---

## 📞 Support

If you encounter issues with the build system:

1. Check GitHub Actions logs
2. Review PyInstaller documentation
3. Check for dependency conflicts
4. Test locally before pushing

The automated build system makes it easy to provide professional-grade software to your users without manual intervention!
