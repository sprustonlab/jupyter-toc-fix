from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import subprocess

class PostInstallCommand(install):
    """Post-installation script to apply TOC CSS fix and enable extensions."""

    def run(self):
        install.run(self)

        print(f"\n{'='*60}")
        print("jupyter-toc-fix: Setting up Jupyter extensions...")
        print(f"{'='*60}\n")

        # Get Jupyter config directory (respects JUPYTER_CONFIG_DIR env var)
        jupyter_config = os.environ.get('JUPYTER_CONFIG_DIR')

        if not jupyter_config:
            # Fallback to conda prefix if in conda environment
            conda_prefix = os.environ.get('CONDA_PREFIX')
            if conda_prefix:
                jupyter_config = os.path.join(conda_prefix, 'etc', 'jupyter')
            else:
                jupyter_config = os.path.expanduser('~/.jupyter')

        # Step 1: Install nbextensions
        print("[1/3] Installing nbextensions...")
        try:
            subprocess.run(
                ['jupyter', 'contrib', 'nbextension', 'install', '--sys-prefix'],
                check=True,
                capture_output=True
            )
            print("      ✓ nbextensions installed")
        except subprocess.CalledProcessError as e:
            print(f"      ⚠ Warning: Could not install nbextensions: {e}")
        except FileNotFoundError:
            print("      ⚠ Warning: jupyter command not found, skipping nbextensions install")

        # Step 2: Enable configurator
        print("[2/3] Enabling configurator...")
        try:
            subprocess.run(
                ['jupyter', 'nbextensions_configurator', 'enable', '--sys-prefix'],
                check=True,
                capture_output=True
            )
            print("      ✓ configurator enabled")
        except subprocess.CalledProcessError as e:
            print(f"      ⚠ Warning: Could not enable configurator: {e}")
        except FileNotFoundError:
            pass  # Already reported above

        # Step 3: Enable specific extensions
        print("[3/3] Enabling specific extensions...")
        extensions = [
            'toc2/main',
            'collapsible_headings/main',
            'hide_input_all/main',
            'init_cell/main',
            'codefolding/main'
        ]

        for ext in extensions:
            try:
                subprocess.run(
                    ['jupyter', 'nbextension', 'enable', ext, '--sys-prefix'],
                    check=True,
                    capture_output=True
                )
                print(f"      ✓ {ext}")
            except subprocess.CalledProcessError as e:
                print(f"      ⚠ Warning: Could not enable {ext}: {e}")
            except FileNotFoundError:
                pass  # Already reported above

        # Step 4: Apply CSS fix
        print("\n[4/4] Applying TOC positioning fix...")
        custom_dir = os.path.join(jupyter_config, 'custom')
        os.makedirs(custom_dir, exist_ok=True)

        custom_css_path = os.path.join(custom_dir, 'custom.css')

        css_fix = """
/* Fix TOC2 positioning - prevents it from being hidden behind header */
/* Applied by jupyter-toc-fix package v0.2.1 */
#toc-wrapper {
    position: relative !important;
    top: 130px !important;
    left: 0px !important;
}

#notebook-container {
    width: 95% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}
"""

        # Append to custom.css (don't overwrite existing customizations)
        with open(custom_css_path, 'a') as f:
            f.write(css_fix)

        print(f"      ✓ CSS fix applied to: {custom_css_path}")
        print(f"\n{'='*60}")
        print("jupyter-toc-fix: Setup complete!")
        print(f"{'='*60}\n")

setup(
    name='jupyter-toc-fix',
    version='0.2.1',
    description='Automatically configures jupyter_contrib_nbextensions with TOC positioning fix',
    author='Spruston Lab',
    url='https://github.com/sprustonlab/jupyter-toc-fix',
    packages=find_packages(),
    python_requires='>=3.6',
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
)
