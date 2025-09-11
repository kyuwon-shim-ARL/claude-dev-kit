"""
Test suite for deployment command flag system
Tests MUST fail initially (TADD approach)
"""

import pytest
from pathlib import Path
import tempfile
import json
from unittest.mock import patch, MagicMock


class TestDeploymentFlags:
    """Test deployment command with various flags and aliases"""
    
    def test_cleanup_flag_skips_git_operations(self):
        """--cleanup flag should only clean, not commit or push"""
        # Given: A deployment command with cleanup flag
        test_args = "--cleanup"
        
        # When: Execute deployment with cleanup flag
        from src.commands.deployment import execute_deployment
        with patch('src.commands.deployment.git_commit_and_push') as mock_git:
            result = execute_deployment(test_args)
        
        # Then: Git operations should NOT be called
        mock_git.assert_not_called()
        
        # And: Cleanup operations should be executed
        assert result['cleanup_executed'] == True
        assert result['files_cleaned'] > 0
        assert result['docs_organized'] == True
        assert result['git_committed'] == False
        assert result['git_pushed'] == False
    
    def test_korean_alias_cleanup_works(self):
        """한글 별칭 --정리 should work same as --cleanup"""
        # Given: Korean alias for cleanup
        test_args = "--정리"
        
        # When: Execute with Korean alias
        from src.commands.deployment import execute_deployment
        result = execute_deployment(test_args)
        
        # Then: Should behave exactly like --cleanup
        assert result['cleanup_executed'] == True
        assert result['git_committed'] == False
        assert result['git_pushed'] == False
    
    def test_repo_flag_only_cleans_repository(self):
        """--repo flag should only clean repository files"""
        # Given: Temporary files and documents to clean
        temp_dir = Path(tempfile.mkdtemp())
        (temp_dir / "test.tmp").write_text("temp")
        (temp_dir / "test.bak").write_text("backup")
        (temp_dir / "docs" / "test.md").mkdir(parents=True, exist_ok=True)
        
        # When: Execute with --repo flag
        from src.commands.deployment import execute_deployment
        result = execute_deployment(f"--repo --path={temp_dir}")
        
        # Then: Only temp files should be cleaned
        assert not (temp_dir / "test.tmp").exists()
        assert not (temp_dir / "test.bak").exists()
        assert (temp_dir / "docs" / "test.md").parent.exists()  # Docs untouched
        assert result['repo_cleaned'] == True
        assert result['docs_organized'] == False
        assert result['stabilized'] == False
    
    def test_docs_flag_only_organizes_documents(self):
        """--docs flag should only organize documentation"""
        # Given: Documents to organize
        temp_dir = Path(tempfile.mkdtemp())
        docs_dir = temp_dir / "docs" / "CURRENT"
        docs_dir.mkdir(parents=True)
        (docs_dir / "completed-task.md").write_text("Done")
        
        # When: Execute with --docs flag
        from src.commands.deployment import execute_deployment
        result = execute_deployment(f"--docs --path={temp_dir}")
        
        # Then: Documents should be archived
        assert not (docs_dir / "completed-task.md").exists()
        assert (temp_dir / "docs" / "archive" / "completed-task.md").exists()
        assert result['docs_organized'] == True
        assert result['repo_cleaned'] == False
        assert result['files_archived'] == 1
    
    def test_dry_run_simulates_without_changes(self):
        """--dry-run should simulate but not make actual changes"""
        # Given: Files that would be changed
        temp_dir = Path(tempfile.mkdtemp())
        test_file = temp_dir / "test.tmp"
        test_file.write_text("should not be deleted")
        
        # When: Execute with --dry-run
        from src.commands.deployment import execute_deployment
        result = execute_deployment(f"--dry-run --path={temp_dir}")
        
        # Then: File should still exist
        assert test_file.exists()
        assert test_file.read_text() == "should not be deleted"
        
        # But: Report should show what would be done
        assert result['simulation'] == True
        assert result['would_clean'] == ['test.tmp']
        assert result['actual_changes'] == []
    
    def test_full_deployment_without_flags(self):
        """No flags should execute full deployment cycle"""
        # When: Execute without any flags
        from src.commands.deployment import execute_deployment
        with patch('src.commands.deployment.git_commit_and_push') as mock_git:
            mock_git.return_value = {'committed': True, 'pushed': True}
            result = execute_deployment("")
        
        # Then: All operations should execute
        assert result['cleanup_executed'] == True
        assert result['docs_organized'] == True
        assert result['stabilized'] == True
        assert result['git_committed'] == True
        assert result['git_pushed'] == True
        mock_git.assert_called_once()
    
    def test_alias_command_routing(self):
        """Test that /정리, /clean map to /배포 --cleanup"""
        # Given: Various alias commands
        aliases = [
            ('/정리', '--cleanup'),
            ('/clean', '--cleanup'),
            ('/c', '--cleanup'),
            ('/레포정리', '--repo'),
            ('/문서정리', '--docs'),
            ('/안정화', '--stabilize')
        ]
        
        from src.commands.deployment import resolve_alias
        
        for alias, expected_flag in aliases:
            # When: Resolve alias
            resolved = resolve_alias(alias)
            
            # Then: Should map to correct flag
            assert resolved == f"/배포 {expected_flag}"
    
    def test_multiple_flags_combination(self):
        """Multiple flags should work together"""
        # When: Execute with multiple flags
        from src.commands.deployment import execute_deployment
        result = execute_deployment("--repo --docs --no-commit")
        
        # Then: Both operations execute but no commit
        assert result['repo_cleaned'] == True
        assert result['docs_organized'] == True
        assert result['git_committed'] == False
    
    def test_cleanup_performance_under_10_seconds(self):
        """Cleanup operations should complete within 10 seconds"""
        import time
        
        # Given: Large number of files to clean
        temp_dir = Path(tempfile.mkdtemp())
        for i in range(100):
            (temp_dir / f"test{i}.tmp").write_text(f"temp{i}")
        
        # When: Execute cleanup
        from src.commands.deployment import execute_deployment
        start_time = time.time()
        result = execute_deployment(f"--cleanup --path={temp_dir}")
        elapsed = time.time() - start_time
        
        # Then: Should complete quickly
        assert elapsed < 10.0
        assert result['files_cleaned'] == 100
        assert all(not (temp_dir / f"test{i}.tmp").exists() for i in range(100))