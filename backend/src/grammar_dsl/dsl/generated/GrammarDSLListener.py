# Generated from C:/GITHUB/Smart-Grammar-Checker-using-DSL-and-Rule-Based-Parsing/backend/src/grammar_dsl/dsl/grammar/GrammarDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .GrammarDSLParser import GrammarDSLParser
else:
    from GrammarDSLParser import GrammarDSLParser

# This class defines a complete listener for a parse tree produced by GrammarDSLParser.
class GrammarDSLListener(ParseTreeListener):

    # Enter a parse tree produced by GrammarDSLParser#command.
    def enterCommand(self, ctx:GrammarDSLParser.CommandContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#command.
    def exitCommand(self, ctx:GrammarDSLParser.CommandContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#grammarCheckCmd.
    def enterGrammarCheckCmd(self, ctx:GrammarDSLParser.GrammarCheckCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#grammarCheckCmd.
    def exitGrammarCheckCmd(self, ctx:GrammarDSLParser.GrammarCheckCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#generateExerciseCmd.
    def enterGenerateExerciseCmd(self, ctx:GrammarDSLParser.GenerateExerciseCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#generateExerciseCmd.
    def exitGenerateExerciseCmd(self, ctx:GrammarDSLParser.GenerateExerciseCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#quantitySpec.
    def enterQuantitySpec(self, ctx:GrammarDSLParser.QuantitySpecContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#quantitySpec.
    def exitQuantitySpec(self, ctx:GrammarDSLParser.QuantitySpecContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#createQuizCmd.
    def enterCreateQuizCmd(self, ctx:GrammarDSLParser.CreateQuizCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#createQuizCmd.
    def exitCreateQuizCmd(self, ctx:GrammarDSLParser.CreateQuizCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#submitAnswersCmd.
    def enterSubmitAnswersCmd(self, ctx:GrammarDSLParser.SubmitAnswersCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#submitAnswersCmd.
    def exitSubmitAnswersCmd(self, ctx:GrammarDSLParser.SubmitAnswersCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#answerEntry.
    def enterAnswerEntry(self, ctx:GrammarDSLParser.AnswerEntryContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#answerEntry.
    def exitAnswerEntry(self, ctx:GrammarDSLParser.AnswerEntryContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#answerSeparator.
    def enterAnswerSeparator(self, ctx:GrammarDSLParser.AnswerSeparatorContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#answerSeparator.
    def exitAnswerSeparator(self, ctx:GrammarDSLParser.AnswerSeparatorContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#answerValue.
    def enterAnswerValue(self, ctx:GrammarDSLParser.AnswerValueContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#answerValue.
    def exitAnswerValue(self, ctx:GrammarDSLParser.AnswerValueContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#showStudentsCmd.
    def enterShowStudentsCmd(self, ctx:GrammarDSLParser.ShowStudentsCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#showStudentsCmd.
    def exitShowStudentsCmd(self, ctx:GrammarDSLParser.ShowStudentsCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#showResultsCmd.
    def enterShowResultsCmd(self, ctx:GrammarDSLParser.ShowResultsCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#showResultsCmd.
    def exitShowResultsCmd(self, ctx:GrammarDSLParser.ShowResultsCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#showQuizCmd.
    def enterShowQuizCmd(self, ctx:GrammarDSLParser.ShowQuizCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#showQuizCmd.
    def exitShowQuizCmd(self, ctx:GrammarDSLParser.ShowQuizCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#showClassCmd.
    def enterShowClassCmd(self, ctx:GrammarDSLParser.ShowClassCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#showClassCmd.
    def exitShowClassCmd(self, ctx:GrammarDSLParser.ShowClassCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#studentFilterExpr.
    def enterStudentFilterExpr(self, ctx:GrammarDSLParser.StudentFilterExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#studentFilterExpr.
    def exitStudentFilterExpr(self, ctx:GrammarDSLParser.StudentFilterExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#studentFilterOrExpr.
    def enterStudentFilterOrExpr(self, ctx:GrammarDSLParser.StudentFilterOrExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#studentFilterOrExpr.
    def exitStudentFilterOrExpr(self, ctx:GrammarDSLParser.StudentFilterOrExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#studentFilterAndExpr.
    def enterStudentFilterAndExpr(self, ctx:GrammarDSLParser.StudentFilterAndExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#studentFilterAndExpr.
    def exitStudentFilterAndExpr(self, ctx:GrammarDSLParser.StudentFilterAndExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#studentFilterPrimary.
    def enterStudentFilterPrimary(self, ctx:GrammarDSLParser.StudentFilterPrimaryContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#studentFilterPrimary.
    def exitStudentFilterPrimary(self, ctx:GrammarDSLParser.StudentFilterPrimaryContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#comparisonExpr.
    def enterComparisonExpr(self, ctx:GrammarDSLParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#comparisonExpr.
    def exitComparisonExpr(self, ctx:GrammarDSLParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#statusExpr.
    def enterStatusExpr(self, ctx:GrammarDSLParser.StatusExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#statusExpr.
    def exitStatusExpr(self, ctx:GrammarDSLParser.StatusExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#revisionPlanCmd.
    def enterRevisionPlanCmd(self, ctx:GrammarDSLParser.RevisionPlanCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#revisionPlanCmd.
    def exitRevisionPlanCmd(self, ctx:GrammarDSLParser.RevisionPlanCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#historyCmd.
    def enterHistoryCmd(self, ctx:GrammarDSLParser.HistoryCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#historyCmd.
    def exitHistoryCmd(self, ctx:GrammarDSLParser.HistoryCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#resetHistoryCmd.
    def enterResetHistoryCmd(self, ctx:GrammarDSLParser.ResetHistoryCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#resetHistoryCmd.
    def exitResetHistoryCmd(self, ctx:GrammarDSLParser.ResetHistoryCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#spellCmd.
    def enterSpellCmd(self, ctx:GrammarDSLParser.SpellCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#spellCmd.
    def exitSpellCmd(self, ctx:GrammarDSLParser.SpellCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#verbCmd.
    def enterVerbCmd(self, ctx:GrammarDSLParser.VerbCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#verbCmd.
    def exitVerbCmd(self, ctx:GrammarDSLParser.VerbCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#synonymCmd.
    def enterSynonymCmd(self, ctx:GrammarDSLParser.SynonymCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#synonymCmd.
    def exitSynonymCmd(self, ctx:GrammarDSLParser.SynonymCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#helpCmd.
    def enterHelpCmd(self, ctx:GrammarDSLParser.HelpCmdContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#helpCmd.
    def exitHelpCmd(self, ctx:GrammarDSLParser.HelpCmdContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#featureExpr.
    def enterFeatureExpr(self, ctx:GrammarDSLParser.FeatureExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#featureExpr.
    def exitFeatureExpr(self, ctx:GrammarDSLParser.FeatureExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#featureOrExpr.
    def enterFeatureOrExpr(self, ctx:GrammarDSLParser.FeatureOrExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#featureOrExpr.
    def exitFeatureOrExpr(self, ctx:GrammarDSLParser.FeatureOrExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#featureAndExpr.
    def enterFeatureAndExpr(self, ctx:GrammarDSLParser.FeatureAndExprContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#featureAndExpr.
    def exitFeatureAndExpr(self, ctx:GrammarDSLParser.FeatureAndExprContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#featurePrimary.
    def enterFeaturePrimary(self, ctx:GrammarDSLParser.FeaturePrimaryContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#featurePrimary.
    def exitFeaturePrimary(self, ctx:GrammarDSLParser.FeaturePrimaryContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#featureAtom.
    def enterFeatureAtom(self, ctx:GrammarDSLParser.FeatureAtomContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#featureAtom.
    def exitFeatureAtom(self, ctx:GrammarDSLParser.FeatureAtomContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#tense.
    def enterTense(self, ctx:GrammarDSLParser.TenseContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#tense.
    def exitTense(self, ctx:GrammarDSLParser.TenseContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#aspect.
    def enterAspect(self, ctx:GrammarDSLParser.AspectContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#aspect.
    def exitAspect(self, ctx:GrammarDSLParser.AspectContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#voice.
    def enterVoice(self, ctx:GrammarDSLParser.VoiceContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#voice.
    def exitVoice(self, ctx:GrammarDSLParser.VoiceContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#sentenceType.
    def enterSentenceType(self, ctx:GrammarDSLParser.SentenceTypeContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#sentenceType.
    def exitSentenceType(self, ctx:GrammarDSLParser.SentenceTypeContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#clauseStructure.
    def enterClauseStructure(self, ctx:GrammarDSLParser.ClauseStructureContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#clauseStructure.
    def exitClauseStructure(self, ctx:GrammarDSLParser.ClauseStructureContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#grammaticalFeature.
    def enterGrammaticalFeature(self, ctx:GrammarDSLParser.GrammaticalFeatureContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#grammaticalFeature.
    def exitGrammaticalFeature(self, ctx:GrammarDSLParser.GrammaticalFeatureContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#paragraph.
    def enterParagraph(self, ctx:GrammarDSLParser.ParagraphContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#paragraph.
    def exitParagraph(self, ctx:GrammarDSLParser.ParagraphContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#sentence.
    def enterSentence(self, ctx:GrammarDSLParser.SentenceContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#sentence.
    def exitSentence(self, ctx:GrammarDSLParser.SentenceContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#sentencePart.
    def enterSentencePart(self, ctx:GrammarDSLParser.SentencePartContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#sentencePart.
    def exitSentencePart(self, ctx:GrammarDSLParser.SentencePartContext):
        pass


    # Enter a parse tree produced by GrammarDSLParser#sentenceTerminator.
    def enterSentenceTerminator(self, ctx:GrammarDSLParser.SentenceTerminatorContext):
        pass

    # Exit a parse tree produced by GrammarDSLParser#sentenceTerminator.
    def exitSentenceTerminator(self, ctx:GrammarDSLParser.SentenceTerminatorContext):
        pass



del GrammarDSLParser